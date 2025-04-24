# Use Python 3.10 as base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files (excluding frontend and demos)
COPY main.py .
COPY search.py .
COPY prompt_templates.py .
COPY createDatabase.py .
COPY .env .

# Expose port
EXPOSE 8888

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8888"] 