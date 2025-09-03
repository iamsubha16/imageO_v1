FROM python:3.12.1

# Set working directory
WORKDIR /app

# Install OS-level dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Create a consistent non-root user with known UID (1000) and GID (1000)
RUN groupadd -g 1000 appgroup && useradd -u 1000 -g appgroup -m appuser

# Create cache directories and set correct ownership and permissions
RUN mkdir -p /app/.cache /app/.u2net && \
    chown -R appuser:appgroup /app/.cache /app/.u2net && \
    chmod -R 755 /app/.cache /app/.u2net

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --no-warn-script-location -r requirements.txt

# Copy the rest of your app code
COPY . .

# Change ownership of everything to appuser
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Expose port for HF Spaces
EXPOSE 7860

# Launch app
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "app:app"]
# CMD ["gunicorn", "--bind", "0.0.0.0:7860", "--workers", "2", "--threads", "1", "--worker-class", "gthread", "--timeout", "600", "--max-requests", "1000", "--max-requests-jitter", "100", "--worker-tmp-dir", "/dev/shm", "--preload", "app:app"]
