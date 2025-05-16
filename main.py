from fastapi import FastAPI, HTTPException, Request, status, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional
import datetime
import string
import random
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="URL Shortener",
    description="A URL shortener service with web UI built with FastAPI",
    version="1.0.0"
)


app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


class URLBase(BaseModel):
    target_url: str = Field(..., description="The original URL to be shortened")
    
    @validator('target_url')
    def validate_url(cls, v):
        
        if not v.startswith(('http://', 'https://')):
            raise ValueError('URL must start with http:// or https://')
        return v

class URLCreate(URLBase):
    pass

class URLInfo(URLBase):
    id: str = Field(..., description="Unique identifier for the shortened URL")
    short_url: str = Field(..., description="The shortened URL")
    created_at: datetime.datetime = Field(..., description="When the shortened URL was created")
    clicks: int = Field(default=0, description="Number of times the shortened URL has been accessed")

    class Config:
        schema_extra = {
            "example": {
                "target_url": "https://www.example.com/very/long/path/to/resource",
                "id": "abc123",
                "short_url": "/abc123",
                "created_at": "2023-05-15T10:30:00",
                "clicks": 5
            }
        }

# In-memory database
url_db: Dict[str, URLInfo] = {}
# Counter for generating sequential IDs
counter = 1000000  

# Characters used for base62 encoding 
CHARACTERS = string.digits + string.ascii_lowercase + string.ascii_uppercase

# create a short URL using base62 encoding
def encode_base62(num):
    """Convert a decimal number to base62 string."""
    if num == 0:
        return CHARACTERS[0]
    
    result = ""
    base = len(CHARACTERS)
    
    while num:
        num, remainder = divmod(num, base)
        result = CHARACTERS[remainder] + result
        
    return result

def create_short_code():
    
    global counter
    counter += 1
    return encode_base62(counter)

# API endpoints
@app.get("/", response_class=HTMLResponse, tags=["UI"])
async def home_page(request: Request):
  
    urls = list(url_db.values())
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "urls": urls}
    )

@app.post("/", response_class=HTMLResponse, tags=["UI"])
async def create_url_ui(request: Request, target_url: str = Form(...)):
    """
    Create a shortened URL from the web UI form.
    """
    try:
        # Validate URL
        url_create = URLCreate(target_url=target_url)
        
        
        url_id = create_short_code()
        
        
        short_url = f"/{url_id}"
        
        
        url_info = URLInfo(
            target_url=url_create.target_url,
            id=url_id,
            short_url=short_url,
            created_at=datetime.datetime.now(),
            clicks=0
        )
        
        
        url_db[url_id] = url_info
        
        
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    
    except ValueError as e:
        
        urls = list(url_db.values())
        return templates.TemplateResponse(
            "index.html", 
            {
                "request": request, 
                "urls": urls, 
                "error": str(e),
                "target_url": target_url
            }
        )

@app.get("/details/{url_id}", response_class=HTMLResponse, tags=["UI"])
async def url_details_page(request: Request, url_id: str):
    """
    Show details page for a specific URL.
    """
    if url_id not in url_db:
        return templates.TemplateResponse(
            "error.html", 
            {"request": request, "message": f"URL with ID {url_id} not found"}
        )
    
    url_info = url_db[url_id]
    return templates.TemplateResponse(
        "details.html", 
        {"request": request, "url": url_info}
    )

@app.post("/delete/{url_id}", tags=["UI"])
async def delete_url_ui(url_id: str):
    """
    Delete a URL from the web UI.
    """
    if url_id not in url_db:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    
    
    del url_db[url_id]
    
    # Redirect back to home page
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/{url_id}", tags=["Redirects"])
async def redirect_to_target_url(url_id: str, request: Request):
    """
    Redirect to the target URL.
    
    - **url_id**: The ID of the shortened URL
    
    Redirects to the original URL if found, otherwise shows an error page.
    """
    if url_id not in url_db:
        return templates.TemplateResponse(
            "error.html", 
            {"request": request, "message": f"URL with ID {url_id} not found"}
        )
    
    # Increment click count
    url_db[url_id].clicks += 1
    
    # Redirect to the target URL
    return RedirectResponse(url=url_db[url_id].target_url)


@app.post("/api/url", response_model=URLInfo, status_code=status.HTTP_201_CREATED, tags=["API"])
async def create_url_api(url: URLCreate):
    """
    Create a shortened URL via API.
    
    - **target_url**: The original URL to be shortened
    
    Returns the shortened URL information.
    """
    # Generate a short code for the URL
    url_id = create_short_code()
    
    
    short_url = f"/{url_id}"
    
    # Create URL info
    url_info = URLInfo(
        target_url=url.target_url,
        id=url_id,
        short_url=short_url,
        created_at=datetime.datetime.now(),
        clicks=0
    )
    
   
    url_db[url_id] = url_info
    
    return url_info

@app.get("/api/url/{url_id}", response_model=URLInfo, tags=["API"])
async def get_url_info_api(url_id: str):
    """
    Get information about a shortened URL via API.
    
    
    
    Returns information about the shortened URL if found, otherwise raises a 404 error.
    """
    if url_id not in url_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"URL with ID {url_id} not found"
        )
    
    return url_db[url_id]

@app.get("/api/urls", response_model=List[URLInfo], tags=["API"])
async def get_all_urls_api():
    """
    Get all shortened URLs via API.
    
  
    """
    return list(url_db.values())

@app.delete("/api/url/{url_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["API"])
async def delete_url_api(url_id: str):
    """
    Delete a shortened URL via API.
    
   
    
    Returns no content if successful, otherwise raises a 404 error.
    """
    if url_id not in url_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"URL with ID {url_id} not found"
        )
    
    # Remove the URL from the database
    del url_db[url_id]
    
    return None

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns a simple message indicating the API is running.
    """
    return {
        "status": "healthy",
        "message": "URL Shortener API is running",
        "urls_count": len(url_db)
    }


sample_urls = [
    "https://fastapi.tiangolo.com/",
    "https://docs.python.org/3/",
    "https://www.python.org/"
]

for url in sample_urls:
    url_id = create_short_code()
    url_db[url_id] = URLInfo(
        target_url=url,
        id=url_id,
        short_url=f"/{url_id}",
        created_at=datetime.datetime.now(),
        clicks=0
    )

if __name__ == "__main__":
    
    print("Starting URL Shortener...")
    print("Web UI will be available at http://localhost:8000")
    print("API documentation will be available at http://localhost:8000/docs")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)