# Base image
FROM python:3.12-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    npm \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy NodeJS deps (FIXED HERE)
COPY package.json package-lock.json ./
RUN npm install

# Copy Tailwind config and input (pastikan input.css ada)
COPY tailwind.config.js ./tailwind.config.js
COPY static/src/input.css ./static/src/input.css
RUN npx tailwindcss -i ./static/src/input.css -o ./static/dist/output.css --minify

# Copy all source code
COPY . .

# Expose port
EXPOSE 8000

# Start Gunicorn
CMD ["gunicorn", "app:app", "--config", "gunicorn.conf.py"]