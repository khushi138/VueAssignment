# Use official Python image as base
FROM python:3.12.1

# Set working directory
WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port (if your Flask app runs on a specific port)
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
