# Use an official Python runtime as a parent image
FROM python:3.9-slim
# Set the working directory
WORKDIR /app
# Install system dependencies (needed for compiling some python packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
# Copy requirements file and install dependencies
COPY requirements.txt .
# We only need the backend dependencies here. For a truly scalable system
# we'd split requirements.txt, but for now we install all.
RUN pip install --no-cache-dir -r requirements.txt
# Download the spacy model
RUN python -m spacy download en_core_web_sm
# Copy the entire project directory into the container
COPY . .
# Expose the API port
EXPOSE 8000
# Run FastAPI server
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
