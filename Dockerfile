# Use Python base image
FROM python:3.8-slim

# Set working directory in the container
WORKDIR /app

# Copy requirements and app code
COPY requirements.txt .
COPY server.py .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable for server ID
ENV SERVER_ID="1"

# Expose the port that the server runs on
EXPOSE 5000

# Command to run the server
CMD ["python", "server.py"]
