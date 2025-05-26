FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy dependency definitions
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8080

# Set the entry point to run the application
CMD ["gunicorn", "-b", "0.0.0.0:8080", "src.main:app"]