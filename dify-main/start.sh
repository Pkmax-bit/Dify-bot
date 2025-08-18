#!/bin/bash

# Navigate to api directory
cd api

# Run database migrations
python run_migration.py

# Start the application
gunicorn --worker-class gevent --workers 1 --worker-connections 1000 --preload --max-requests 1000 --max-requests-jitter 50 --timeout 200 --bind 0.0.0.0:$PORT app:app
