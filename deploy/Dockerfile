FROM python:3.10-slim

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

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN python manage.py collectstatic --noinput

CMD gunicorn TCP_facial_recognition_project.wsgi \
    --workers 2 \
    --threads 4 \
    --timeout 120