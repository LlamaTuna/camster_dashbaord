# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project into the container
COPY . /app/

# Run database migrations and collect static files 
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Expose port 8000 for the Django app
EXPOSE 8000

# Run the Django application using Gunicorn
CMD ["gunicorn", "--config", "gunicorn.conf.py", "camster_dashboard.wsgi:application"]
