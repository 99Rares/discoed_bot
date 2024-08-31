# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app

# Make sure .env is included
COPY .env /app/.env

# Expose necessary ports (if any)
EXPOSE 8080

# Define environment variable for the bot token (optional, as it's in .env)
ENV BOT_TOKEN=your_default_token_here

# Run the bot
CMD ["python", "main.py"]
