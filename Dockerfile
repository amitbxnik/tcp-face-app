# Use a lightweight Python image
FROM python:3.10-slim

# Install system dependencies for dlib, OpenCV, and static file support
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libboost-all-dev \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgl1 \
    libglib2.0-0 \
    ffmpeg \
  && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy in your Django project
COPY . .

# Install Python requirements
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Collect static assets
RUN python manage.py collectstatic --noinput

# Start the server: 1 threaded worker, longer timeout for heavy imports
CMD gunicorn TCP_facial_recognition_project.wsgi \
    --workers 1 \
    --worker-class gthread \
    --threads 2 \
    --timeout 300
