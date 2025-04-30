# Use the slim Python image
FROM python:3.10-slim

# Install system packages for dlib, OpenCV, staticfiles, and threading
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

# Copy your code
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Collect static assets
RUN python manage.py collectstatic --noinput

# Launch Gunicorn with 1 threaded worker and a longer timeout
CMD ["gunicorn", "TCP_facial_recognition_project.wsgi", "--workers", "1", "--worker-class", "gthread", "--threads", "2", "--timeout", "300"]
