#!/bin/bash

# Build script for Render deployment
echo "Starting build process..."

# Upgrade pip first
pip install --upgrade pip

# Install packages with no cache to avoid issues
pip install --no-cache-dir -r requirements.txt

echo "Build completed successfully!" 