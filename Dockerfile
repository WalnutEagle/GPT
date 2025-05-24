# Use official Python runtime
FROM python:3.9-slim

# Set working directory
WORKDIR /opt/app-root/src

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY . .

# Expose port
EXPOSE 8080

# Run the app with Gunicorn
CMD ["gunicorn", "wsgi:application", "--bind", "0.0.0.0:8080"]