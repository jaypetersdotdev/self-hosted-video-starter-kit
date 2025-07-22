# --- Python Builder Stage ---
# This stage's only job is to pre-compile the slow Python packages.
FROM python:3.11-slim-bullseye as python-builder

# Install pip dependencies.
RUN pip install --no-cache-dir torch numba openai-whisper

# --- Final Runtime Stage ---
# Start with an official Node.js image, since n8n is our main application.
# **THE FIX:** Corrected the typo in the image tag name.
FROM node:20-bullseye-slim

# Install runtime dependencies: Python and FFmpeg.
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install n8n directly in the final image.
RUN npm install -g n8n@latest

# Copy the pre-compiled Python packages from the builder stage.
COPY --from=python-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy the whisper executable from the builder.
COPY --from=python-builder /usr/local/bin/whisper /usr/local/bin/whisper

# --- Security & User Setup ---
RUN useradd --create-home --shell /bin/bash appuser

# Create the .n8n directory and set correct ownership.
RUN mkdir -p /home/appuser/.n8n && chown -R appuser:appuser /home/appuser

# Ensure the appuser owns all the globally installed packages.
RUN chown -R appuser:appuser /usr/local/lib/node_modules /usr/local/bin/n8n
RUN chown -R appuser:appuser /usr/local/lib/python3.11/site-packages /usr/local/bin/whisper

# Switch to the non-root user.
USER appuser
WORKDIR /home/appuser

# --- Container Configuration ---
EXPOSE 5678
CMD ["n8n"]