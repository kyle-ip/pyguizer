# Deployment

PyGUIzer provides multiple options for deploying your applications, from simple local execution to containerized production deployments. Choose the method that best fits your needs.

## Packaging as Standalone Executable

PyGUIzer can package your application into a single executable file that can be run anywhere without Python or dependencies:

```bash
# Basic packaging
python -m pyguizer package app.py

# Custom name and output directory
python -m pyguizer package app.py --name my_app --output_dir ./dist

# With console window for debugging
python -m pyguizer package app.py --windowed false
```

### Package Options

| Option | Description | Default |
|--------|-------------|---------|
| `name` | Name for the executable | Same as input file name |
| `output_dir` | Output directory for the executable | `./dist` |
| `onefile` | Create a single-file executable | `True` |
| `windowed` | Create a windowed (GUI) executable without console | `True` |

### How It Works

1. PyGUIzer uses PyInstaller to bundle your application
2. It includes all necessary dependencies
3. The executable starts a local server automatically
4. Your browser opens to show the GUI
5. No Python installation required

## Docker Deployment

PyGUIzer includes Docker support for containerized deployments:

### Using docker-compose

The simplest way to run PyGUIzer with Docker is using `docker-compose`:

```bash
# Build and run
 docker-compose up --build

# Run in detached mode
docker-compose up --build -d
```

### Manual Docker Build

You can also build and run Docker containers manually:

```bash
# Build the image
docker build -t pyguizer .

# Run the container
docker run -p 8000:8000 pyguizer

# Run with volume mount for development
docker run -p 8000:8000 -v $(pwd):/app pyguizer
```

### Docker Configuration

PyGUIzer's Docker setup includes:

- **Python 3.11-slim** base image for minimal size
- **Node.js 18** for frontend builds
- **Automatic frontend build** during container creation
- **Port 8000** exposed for web access
- **Default app creation** if no app.py exists

## Web Server Deployment

For production web server deployments:

### Using a Reverse Proxy

Deploy behind a reverse proxy like Nginx or Apache:

```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### Using Gunicorn

Run with Gunicorn for better performance:

```bash
pip install gunicorn uvicorn

# Run with 4 workers
gunicorn -w 4 -k uvicorn.workers.UvicornWorker pyguizer.api.app:create_app
```

## Cloud Deployment

PyGUIzer applications can be deployed to various cloud platforms:

### Heroku

```bash
# Create a Procfile
cat > Procfile << 'EOF'
web: python -m pyguizer run app.py --host 0.0.0.0 --port $PORT
EOF

# Deploy to Heroku
git push heroku main
```

### AWS

Deploy to AWS using EC2, ECS, or Lambda:

- **EC2**: Run as a regular web service
- **ECS**: Use the Docker container
- **Lambda**: For serverless deployments (requires additional configuration)

## Environment Variables

PyGUIzer supports the following environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `PYTHONUNBUFFERED` | Disable output buffering | `1` (enabled) |
| `PYGUIZER_HOST` | Host to bind the server | `0.0.0.0` |
| `PYGUIZER_PORT` | Port to bind the server | `8000` |
| `PYGUIZER_TITLE` | Application title | `PyGUIzer App` |

## Best Practices

1. **Security**: Always validate user input, especially for file uploads
2. **Performance**: Use appropriate widget types for large inputs
3. **Scalability**: Consider using a production WSGI server for high traffic
4. **Reliability**: Set up proper error handling and logging
5. **Maintainability**: Document your application and its dependencies
