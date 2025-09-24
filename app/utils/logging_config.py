import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from flask import request, g
import time

def setup_logging(app):
    # Remove default handlers to prevent duplicate logs
    if app.logger.hasHandlers():
        app.logger.handlers.clear()

    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    # Set up file handler with rotation
    file_handler = RotatingFileHandler(
        'logs/milk_detector.log',
        maxBytes=10240000,  # 10MB
        backupCount=10
    )
    
    # Create formatter with local time
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s [%(pathname)s:%(lineno)d]: %(message)s'
    )
    formatter.converter = time.localtime  # use local time
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    
    # Set up console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    
    # Configure app logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.INFO)
    
    # Set up request logging
    @app.before_request
    def log_request_info():
        g.start_time = time.time()
        app.logger.info(
            f"Request started - {request.method} {request.url} - "
            f"IP: {request.remote_addr} - User-Agent: {request.headers.get('User-Agent', 'Unknown')}"
        )
    
    @app.after_request
    def log_response_info(response):
        duration = time.time() - g.start_time if hasattr(g, 'start_time') else 0
        app.logger.info(
            f"Request completed - {request.method} {request.url} - "
            f"Status: {response.status_code} - Duration: {duration:.3f}s"
        )
        return response
