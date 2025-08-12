#!/bin/bash

# Start the ATIM backend with proper environment setup

echo "🚀 Starting Atim Backend Server..."

# Set up temporary directory
export TMPDIR=/Users/ochiengodero/tmp
mkdir -p $TMPDIR

# Activate virtual environment
source venv/bin/activate

# Start the Flask application
python app.py 