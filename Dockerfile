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

# Copy requirements (only these first for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy rest of the project
COPY . .

# Set default user
RUN useradd -ms /bin/bash vscode
USER vscode

CMD [ "bash" ]