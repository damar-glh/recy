# Base image
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    npm \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy NodeJS config for Tailwind CSS
COPY package.json package-lock.json tailwind.config.js input.css ./
RUN npm install
RUN npx tailwindcss -i ./input.css -o ./static/output.css --minify

# Copy source code
COPY . .

# Expose port used by Gunicorn
EXPOSE 8000

# Default command to run Gunicorn
CMD ["gunicorn", "app:app", "--config", "gunicorn.conf.py"]