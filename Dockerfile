# Use official Python base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy project files into the container
COPY . /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port 8000 for Django app
EXPOSE 8000

# Command to run the Django app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "hello_world_project.wsgi:application"]