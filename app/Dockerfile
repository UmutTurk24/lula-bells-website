# Use an official Python runtime as a base (or whatever base image your app uses)
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs

# Copy the application code to the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Node.js packages
RUN npm install -g npx --force && npm install --force

# Run the Tailwind CSS build command
RUN npx tailwindcss -i ./static/src/input.css -o ./static/dist/css/output.css --watch &

# Expose the port your app runs on
EXPOSE 5000

CMD ["python", "main.py"]
# CMD ["echo", "Hello, World!"]
