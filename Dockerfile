# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for the app
EXPOSE 8000

# Define the command to run the app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
