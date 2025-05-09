#!/bin/bash

# Luxury Marketing Analytics Dashboard Launcher

echo "Starting Luxury Marketing Analytics Dashboard..."

# Check if Node.js is installed
if command -v node &> /dev/null; then
    # Use Node.js server
    echo "Using Node.js server"
    npm install
    node server.js
else
    # Fall back to Python server
    echo "Node.js not found, falling back to Python server"
    
    # Check for Python version
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        echo "Error: Neither Node.js nor Python is installed. Please install one of them to run the server."
        exit 1
    fi
    
    # Start Python server
    echo "Starting Python HTTP server on port 8000..."
    cd dashboard
    $PYTHON_CMD -m http.server 8000
fi