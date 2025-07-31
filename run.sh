#!/bin/bash
echo "Start Deployment..."
docker compose down
docker compose up -d --build
docker compose ps