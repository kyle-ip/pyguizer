# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js for frontend build
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
RUN apt-get install -y nodejs

# Copy requirements files
COPY pyproject.toml .
COPY package.json ./frontend/
COPY package-lock.json ./frontend/

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -e .

# Install frontend dependencies and build frontend
RUN cd frontend && npm install && npm run build

# Copy application code
COPY . .

# Create a default app.py if it doesn't exist
RUN if [ ! -f "/app/app.py" ]; then \
    echo "from pyguizer import PyGUIzer\n\n@PyGUIzer()\ndef add(a: int, b: int) -> int:\n    \"\"\"Add two numbers together.\"\"\"\n    return a + b\n\n@PyGUIzer()\ndef greet(name: str, age: int) -> str:\n    \"\"\"Generate a greeting message.\"\"\"\n    return f\"Hello, {name}! You are {age} years old.\"\n" > /app/app.py; \
    fi

# Expose port 8000
EXPOSE 8000

# Command to run the application
CMD ["python", "-m", "pyguizer", "run", "app.py", "--host", "0.0.0.0", "--port", "8000"]