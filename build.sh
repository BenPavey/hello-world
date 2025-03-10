#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

#Runs Django’s collectstatic command, which:
	#Finds all static files from STATICFILES_DIRS.
	#Copies them to STATIC_ROOT (staticfiles/).
	#WhiteNoise serves these files in production.
✅ Why --no-input?
	#This prevents any user prompts (e.g., confirmation messages).
	#Render runs this automatically, so it must run without requiring input.
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate