#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Step 1: Setup Python virtual environment
echo "Setting up Python virtual environment..."
if command -v python &>/dev/null; then
    python -m venv venv
else
    python3 -m venv venv
fi

source venv/bin/activate


# Step 2: Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt


# Step 3: Install plugins from ./plugins
echo "Installing plugins..."
pip install ./plugins


# Step 4: Build Docker image
echo "Building Docker image..."
docker build -t airbnb-automation .

echo "Setup complete."