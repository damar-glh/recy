FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    npm \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY package.json package-lock.json ./
RUN npm install
COPY tailwind.config.js ./
COPY static/src/input.css ./static/src/input.css
RUN npx tailwindcss -i ./static/src/input.css -o ./static/dist/output.css --minify

COPY . .

EXPOSE 8000

CMD ["gunicorn", "app:app", "--config", "gunicorn.conf.py"]