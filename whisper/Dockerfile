# Use a base image with Python and common dependencies
FROM python:3.10-slim

# Install FFmpeg AND Git
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg git

# Install Python dependencies for a Whisper web service
RUN pip install "fastapi[all]" uvicorn "git+https://github.com/openai/whisper.git"

# Copy the application code
COPY ./app /app

# Set the working directory
WORKDIR /app

# Expose the port the app will run on
EXPOSE 9000

# Command to run the web service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]