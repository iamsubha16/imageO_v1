# Base image
FROM python:3.12.1

# Set working directory
WORKDIR /app

# Install OS-level dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Create a consistent non-root user
RUN groupadd -g 1000 appgroup && useradd -u 1000 -g appgroup -m appuser

# Create cache directories and set permissions
RUN mkdir -p /app/.cache /app/.u2net && \
    chown -R appuser:appgroup /app/.cache /app/.u2net && \
    chmod -R 755 /app/.cache /app/.u2net

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --no-warn-script-location -r requirements.txt

# Copy compiled Python files (.pyc) only
COPY __pycache__/ ./__pycache__/

# Copy your models
COPY models/ ./models/

# Set ownership to non-root user
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Expose the port for HF Spaces
EXPOSE 7860

# Launch your Flask app from compiled .pyc
CMD ["python", "-m", "__pycache__.run.cpython-312"]
