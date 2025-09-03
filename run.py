import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Production configuration
    port = int(os.environ.get("PORT", 7860))
    debug = False
    
    app.logger.info(f"Starting application on port {port} (debug={'on' if debug else 'off'})")
    
    app.run(
        host="0.0.0.0", 
        port=port,
        debug=debug,
        threaded=True
    )