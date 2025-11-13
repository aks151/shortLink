# Start with a lightweight Python base image
FROM python:3.11-slim

# Install system dependencies required for building Python packages like psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the dependency file first to leverage Docker layer caching
COPY requirements.txt .

# Install dependencies
# --no-cache-dir reduces image size and is a good practice for containers
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and the start script into the container
COPY ./app /app/app
COPY start.sh .

# Make the start script executable inside the container
RUN chmod +x /app/start.sh

# Expose the port the app runs on
EXPOSE 8000

# The command to run the application using the start script
CMD ["/app/start.sh"]
