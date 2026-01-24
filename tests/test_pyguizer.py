from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import our PyGUIzer components
from pyguizer import PyGUIzer
from pyguizer.api.app import create_app

# Define a sample function
@PyGUIzer()
def greet(name: str, age: int, is_active: bool = True) -> str:
    """Generate a greeting message."""
    status_str = "active" if is_active else "inactive"
    return f"Hello {name}! You are {age} years old and {status_str}."

# Create the FastAPI app
app = create_app(greet)

if __name__ == "__main__":
    print("Starting PyGUIzer test server...")
    print("Open http://localhost:8000 in your browser to test the application.")
    uvicorn.run("test_pyguizer:app", host="0.0.0.0", port=8000, reload=False)
