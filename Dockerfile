# Use the official Python slim image as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file (if you have one) or install dependencies directly
# Since your project has minimal dependencies, we'll install them directly
RUN pip install --no-cache-dir flask

# Copy the entire project directory into the container
COPY . .

# Expose port 7860 (Hugging Face Spaces default port, matches your app)
EXPOSE 7860

# Command to run the Flask app
CMD ["python", "main.py"]