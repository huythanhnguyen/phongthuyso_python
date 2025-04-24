"""
ASGI Application

File chứa ứng dụng ASGI để chạy với uvicorn/gunicorn.
"""

from main import app

# Expose app for uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("asgi:app", host="0.0.0.0", port=8000, reload=True) 