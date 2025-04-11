# Use official Python base image
FROM python:3.11-slim

# Set work directory inside the container
WORKDIR /app

# Copy dependency file and install packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY ./app ./app

# Expose the FastAPI port
EXPOSE 8000

# Start the FastAPI app using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
