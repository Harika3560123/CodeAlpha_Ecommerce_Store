#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

# Install production requirements
pip install -r requirements.txt

# Collect static files with WhiteNoise
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate

# Seed catalog products, categories and demo accounts
python seed_data.py
