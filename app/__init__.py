import os
import sys
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import timedelta

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    
    # Load configuration
    from app.config import Config
    app.config.from_object(Config)
    
    # Handle proxy headers
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    
    # Setup logging
    from app.utils.logging_config import setup_logging
    setup_logging(app)
    
    # Initialize services
    try:
        from app.models.models import initialize_models
        from app.services.firebase_service import initialize_firebase
        
        # Store models in app config for global access
        u2net_session, model = initialize_models(app)
        app.config['U2NET_SESSION'] = u2net_session
        app.config['ML_MODEL'] = model
        
        initialize_firebase(app)
        app.logger.info("Application initialization completed successfully")
        
    except Exception as e:
        app.logger.critical(f"Application failed to start: {str(e)}")
        sys.exit(1)
    
    # Register blueprints
    from app.auth.routes import auth_bp
    from app.main.routes import main_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    
    # Register error handlers
    register_error_handlers(app)
    
    return app

def register_error_handlers(app):
    from flask import jsonify
    import traceback
    
    @app.errorhandler(400)
    def bad_request(error):
        app.logger.warning(f"Bad request: {error}")
        return jsonify({'error': 'Bad request'}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        app.logger.warning(f"Unauthorized access: {error}")
        return jsonify({'error': 'Unauthorized'}), 401

    @app.errorhandler(403)
    def forbidden(error):
        app.logger.warning(f"Forbidden access: {error}")
        return jsonify({'error': 'Forbidden'}), 403

    @app.errorhandler(404)
    def not_found(error):
        app.logger.warning(f"Page not found")
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(413)
    def request_entity_too_large(error):
        app.logger.warning(f"File too large")
        return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413

    @app.errorhandler(500)
    def internal_server_error(error):
        app.logger.error(f"Internal server error: {str(error)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': 'Internal server error'}), 500