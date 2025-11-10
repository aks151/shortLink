# ShortLink: FastAPI URL Shortener

ShortLink is a simple and efficient URL shortening service built with Python and FastAPI. It takes a long URL and returns a short, unique link that redirects to the original URL.

## Features

- Fast and asynchronous API built with FastAPI.
- Efficiently handles duplicate URLs by returning existing short links instead of creating new ones.
- Uses SQLAlchemy for asynchronous database interactions.
- Relies on Pydantic for robust data validation.
- Generates short, unique codes for each URL.

## Tech Stack

- Python 3.10+
- FastAPI
- SQLAlchemy (Async)
- Uvicorn (for serving)
- `shortuuid` (for generating short codes)

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd shortLink
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # Create the virtual environment
    python3 -m venv venv

    # Activate it (on macOS/Linux)
    source venv/bin/activate

    # Or on Windows
    # venv\Scripts\activate
    ```

3.  **Install dependencies:**
    Make sure you have a `requirements.txt` file with the necessary packages (fastapi, uvicorn, sqlalchemy, shortuuid, etc.).
    ```bash
    pip install -r requirements.txt
    ```

4.  **Database Setup**
    The application is configured to create the necessary database tables automatically upon startup. By default, it will likely use a local database file (e.g., SQLite).

## How to Run the Application

Once the setup is complete, you can run the application using `uvicorn`.

```bash
uvicorn app.main:app --reload
```

The API will be live at `http://127.0.0.1:8000`. The `--reload` flag enables hot-reloading, so the server will restart automatically after you make code changes.

## API Endpoints

### 1. Create a Short Link

- **Endpoint:** `POST /api/v1/shorten`
- **Description:** Creates a new short link or returns an existing one if the long URL has already been shortened.
- **Request Body:**
  ```json
  {
    "longUrl": "https://www.example.com/a/very/long/url/to/shorten"
  }
  ```
- **Success Response (`200 OK`):**
  ```json
  {
    "longUrl": "https://www.example.com/a/very/long/url/to/shorten",
    "shortLink": "http://127.0.0.1:8000/xxxxxxx"
  }
  ```

### 2. Redirect to Long URL

- **Endpoint:** `GET /{short_code}`
- **Description:** Redirects the user to the original long URL associated with the given `short_code`.
- **Success Response:** `307 Temporary Redirect` to the long URL.
- **Error Response:** `404 Not Found` if the `short_code` does not exist in the database.

## Example Usage (cURL)

Here is an example of how to create a short link using cURL:

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/shorten" \
-H "Content-Type: application/json" \
-d '{"longUrl": "https://github.com/tiangolo/fastapi"}'
```

**Example Response:**

```json
{
  "longUrl": "https://github.com/tiangolo/fastapi",
  "shortLink": "http://127.0.0.1:8000/YpT5sE3"
}
```

