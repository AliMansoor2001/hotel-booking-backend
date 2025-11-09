#!/bin/bash
# Install system dependencies
apt-get update
apt-get install -y build-essential python3-dev

# Upgrade pip and setuptools
pip install --upgrade pip setuptools wheel

# Install requirements with specific flags
pip install -r requirements.txt --no-cache-dir