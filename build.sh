#!/bin/bash

echo "Using Python version:"
python3.11 --version

python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
