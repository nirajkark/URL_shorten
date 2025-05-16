# URL_shorten - Modern URL Shortener

A modern, fast, and elegant URL shortening service built with FastAPI. ShortLink transforms long, unwieldy URLs into short, memorable links that are easy to share.

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.0+-green.svg)](https://fastapi.tiangolo.com/)


## Features

- **Instant URL Shortening**: Convert any long URL into a short, shareable link.
- **User-friendly Web Interface**: Clean, responsive design for desktop and mobile.
- **QR Code Generation**: Automatically generate QR codes for each shortened URL.
- **Click Tracking**: Monitor how many times your shortened links have been clicked.
- **RESTful API**: Programmatically create and manage shortened URLs.
- **Copy to Clipboard**: One-click copying of shortened URLs.
- **Detailed Analytics**: View creation date and usage statistics for each URL.
- **Base62 Encoding**: Industry-standard URL shortening algorithm for optimal link length.


## 🛠️ Technologies

- **FastAPI**: High-performance web framework for building APIs.
- **Pydantic**: Data validation and settings management.
- **Jinja2**: Template engine for the web interface.
- **Uvicorn**: ASGI server for running the application.
- **HTML/CSS/JavaScript**: Frontend interface.
- **qrcode**: Library for generating QR codes.

## 📋 Prerequisites

- Python 3.7+
- pip (Python package manager)

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/nirajkark/URL_shorten.git
cd URL_shorten
```

### 2. Set Up a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install fastapi uvicorn jinja2 pydantic qrcode[pil]
```

### 4. Run the Application

```bash
python main.py
```

- The web UI will be available at `http://localhost:8000`.
- The API documentation will be available at `http://localhost:8000/docs`.

## 🚀 Usage

### Web Interface
1. Open `http://localhost:8000` in your browser.
2. Enter a URL in the form to shorten it.
3. Optionally, specify a custom alias and an expiration date.
4. Submit the form to create a shortened URL.
5. View details of a shortened URL by clicking on its ID, including a QR code.
6. Delete URLs directly from the UI.

### API Endpoints
- **POST /api/url**: Create a shortened URL.
  - Example: `{"target_url": "https://example.com", "custom_alias": "myalias", "expires_at": "2025-12-31T23:59:59"}`
- **GET /api/url/{url_id}**: Get details of a shortened URL.
- **GET /api/urls**: List all shortened URLs.
- **DELETE /api/url/{url_id}**: Delete a shortened URL.
- **GET /health**: Check the API's health status.

### QR Code
- Access the QR code for a shortened URL at `/qr/{url_id}`.
- Displayed on the details page for each URL.

## 📖 Code Structure

- **main.py**: Core application logic, including FastAPI setup, routes, and URL shortening functionality.
- **templates/**: HTML templates for the web interface (e.g., `index.html`, `details.html`, `error.html`).
- **static/**: Static files (CSS, JavaScript, and generated QR code images).

## 🔧 Extending the Project

### Custom Short URLs
- Users can specify a custom alias (3-15 alphanumeric characters) when creating a URL.
- Validation ensures the alias is unique.

### Expiration Dates
- URLs can have an optional expiration date.
- Expired URLs will not redirect and will display an error message.

### QR Code Generation
- QR codes are generated for each shortened URL using the `qrcode` library.
- Accessible via the `/qr/{url_id}` endpoint and displayed on the details page.

### Future Enhancements
- **Persistent Storage**: Replace the in-memory database with SQLite or PostgreSQL.
- **Rate Limiting**: Add rate limiting to prevent API abuse.
- **User Authentication**: Implement user accounts for managing URLs.
- **Advanced Analytics**: Track IP addresses, user agents, and referral sources for clicks.



## 👨‍💻 Author

- **Niraj Kark** - [GitHub](https://github.com/nirajkark)

## 🙌 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the amazing framework.
- [Pydantic](https://pydantic-docs.helpmanual.io/) for robust data validation.
- [qrcode](https://github.com/lincolnloop/python-qrcode) for QR code generation.
