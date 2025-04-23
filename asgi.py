"""
ASGI entry point for the Phong Thủy Số ADK FastAPI application.
This file is used by Render and other ASGI servers to import and run the FastAPI app.
"""

import os
import sys
from dotenv import load_dotenv

# Add the parent directory to sys.path to allow Python to find the module
file_path = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(file_path)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Load environment variables
load_dotenv()

# Import the FastAPI app
from python_adk.main import app

# This variable is what Render and other ASGI servers will look for
application = app

# If you need to run this directly (for debugging)
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 10000))
    uvicorn.run("asgi:application", host="0.0.0.0", port=port, reload=True) 