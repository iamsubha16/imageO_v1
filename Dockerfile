FROM python:3.12.1

WORKDIR /app

# OS dependencies
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# Non-root user
RUN groupadd -g 1000 appgroup && useradd -u 1000 -g appgroup -m appuser
RUN mkdir -p /app/.cache /app/.u2net && chown -R appuser:appgroup /app/.cache /app/.u2net && chmod -R 755 /app/.cache /app/.u2net

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --no-warn-script-location -r requirements.txt

# Compiled Python files
COPY __pycache__/ ./__pycache__/

# ML models
COPY ml_models/ ./ml_models/

# Templates & static assets
COPY templates/ ./templates/
COPY static/ ./static/

# Set ownership & switch user
RUN chown -R appuser:appgroup /app
USER appuser

# Expose port
EXPOSE 7860

# Launch app
CMD ["python", "-m", "__pycache__.run.cpython-312"]
