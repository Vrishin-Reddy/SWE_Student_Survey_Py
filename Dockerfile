FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBUG=False \
    PORT=8080 \
    ALLOWED_HOSTS=*

# Set work directory
WORKDIR /app

# Install system and Python dependencies
COPY requirements.txt .
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config && \
    pip install --upgrade pip && \
    pip install --no-cache-dir gunicorn && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y --auto-remove build-essential gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Expose application port
EXPOSE 8080

# Corrected Gunicorn Command to run the app
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--forwarded-allow-ips=*", "student_survey_project.wsgi:application"]
