# Use a lightweight Python base image
FROM python:3.12-slim

# Avoid interactive prompts during install
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git curl build-essential python3-venv python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /workspace

# Copy requirements first for Docker layer caching
COPY requirements-base.txt requirements.txt

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Create a non-root user (recommended for dev containers)
RUN useradd -ms /bin/bash vscode
USER vscode

# Default command opens a bash shell
CMD ["bash"]