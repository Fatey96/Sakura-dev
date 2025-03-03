"""
Flask application for STIX generation.
"""

import os
import asyncio
from dotenv import load_dotenv
from flask import Flask, render_template, send_from_directory, request, jsonify
from flask_cors import CORS

# Load environment variables from .env file
load_dotenv()

from stix_generator.config import (
    FLASK_SECRET_KEY, FLASK_DEBUG, FLASK_HOST, FLASK_PORT, 
    OPENAI_API_KEY, OUTPUT_DIR
)
from stix_generator.api.routes import api_bp, generate_graph
from stix_generator.utils.logging_utils import setup_logger

# Check if OpenAI API key is set
if not OPENAI_API_KEY:
    import warnings
    warnings.warn("OPENAI_API_KEY not found in environment variables. LLM features will be unavailable.")

# Create output directory if it doesn't exist
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Set up logger
logger = setup_logger("stix_generator.app")

def create_app():
    """Create and configure the Flask application."""
    app = Flask(
        __name__,
        template_folder='stix_generator/templates',
        static_folder='stix_generator/static'
    )
    
    # Configure Flask application
    app.config['SECRET_KEY'] = FLASK_SECRET_KEY
    app.config['DEBUG'] = FLASK_DEBUG
    
    # Configure CORS to allow requests from frontend
    CORS(app)
    
    # Register the API blueprint
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Add a redirect from root to the API
    @app.route('/')
    def index():
        return {"message": "STIX Generator API. Use /api endpoints."}
    
    # Add direct route for generate-graph at root level for backward compatibility
    @app.route('/generate-graph', methods=['POST'])
    def generate_graph_compat():
        # This is just a compatibility wrapper that forwards to the blueprint route
        return generate_graph()
    
    # Flask routes
    @app.route('/select-objects')
    def select_objects():
        """Render the object selection page."""
        return render_template('select_objects.html')

    @app.route('/stix-visualizer')
    def stix_visualizer():
        """Render the STIX visualizer page."""
        return render_template('stix_visualizer.html')

    # Serve static files for React SPA
    @app.route('/<path:path>')
    def serve_static(path):
        """Serve static files for the React app."""
        if os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return render_template('index.html')

    # Global error handler to ensure all errors return JSON
    @app.errorhandler(Exception)
    def handle_error(e):
        """Handle errors and return JSON responses instead of HTML."""
        if hasattr(e, 'code') and e.code == 404:
            return jsonify(error="Route not found", status="error"), 404
        if hasattr(e, 'code') and e.code == 405:
            return jsonify(error="Method not allowed", status="error"), 405
        
        logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
        return jsonify(error=str(e), status="error"), 500

    # Make asyncio work with Flask
    @app.before_request
    async def before_request():
        """Set up asyncio for request handling."""
        pass

    return app

# For direct execution
if __name__ == '__main__':
    try:
        from asgiref.wsgi import WsgiToAsgi
        import uvicorn
        
        logger.info(f"Starting STIX Generator on {FLASK_HOST}:{FLASK_PORT}")
        app = create_app()
        uvicorn.run(
            WsgiToAsgi(app),
            host=FLASK_HOST,
            port=FLASK_PORT,
            log_level="info"
        )
    except ImportError:
        logger.warning("asgiref and uvicorn not found. Running with standard Flask server (async support limited).")
        app = create_app()
        port = int(os.environ.get('PORT', 5000))
        app.run(
            host='0.0.0.0',
            port=port,
            debug=FLASK_DEBUG
        )