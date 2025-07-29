#!/bin/bash

echo "Using Python version:"
python --version

python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
