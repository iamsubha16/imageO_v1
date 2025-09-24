FROM python:3.12.1

WORKDIR /app

# Install OS dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -g 1000 appgroup && useradd -u 1000 -g appgroup -m appuser

# Create cache directories with correct permissions
RUN mkdir -p /app/.cache /app/.u2net \
    && chown -R appuser:appgroup /app/.cache /app/.u2net \
    && chmod -R 755 /app/.cache /app/.u2net

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --no-warn-script-location -r requirements.txt

# Copy the entire app (Python files, ML models, templates, static)
COPY . .

# Compile all Python files inside the container
RUN python -m compileall .

# Set ownership and switch to non-root user
RUN chown -R appuser:appgroup /app
USER appuser

# Expose port for HF Spaces
EXPOSE 7860

# Launch Flask app via run.py
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "run:app"]
