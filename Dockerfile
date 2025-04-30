FROM python:3.10-slim

# Install build tools and system libs needed for OpenCV + dlib
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libboost-all-dev \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgl1 \                         
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run the app with Gunicorn
CMD ["gunicorn", "TCP_facial_recognition_project.wsgi"]
