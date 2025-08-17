# Use a lightweight Python base image
FROM python:3.12-slim
RUN pip install --upgrade pip

# Create app directory
RUN set -ex && mkdir /tomjerrydetector

# Set working directory inside container
WORKDIR /tomjerrydetector

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libopenblas-dev \
    gfortran \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY model ./model
COPY static ./static
COPY templates ./templates
COPY . .

# Expose Flask port
EXPOSE 8000

# Set environment variables for Flask
ENV PYTHONPATH=/tomjerrydetector

# Start the Flask app
CMD ["python3", "/tomjerrydetector/app.py"]