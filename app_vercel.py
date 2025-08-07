"""
Vercel-optimized Flask application for yt-dlp API
"""
import os
import logging
from flask import Flask, render_template, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging for Vercel
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "vercel-fallback-secret-key")

# Add ProxyFix for Vercel deployment
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Import Vercel-optimized API routes
try:
    from api_vercel import api_bp
    app.register_blueprint(api_bp)
    logging.info("Vercel API blueprint registered successfully")
except ImportError as e:
    logging.error(f"Failed to import Vercel API blueprint: {e}")
    # Fallback to regular API if available
    try:
        from api import api_bp
        app.register_blueprint(api_bp, url_prefix='/api')
        logging.info("Regular API blueprint registered as fallback")
    except ImportError:
        logging.error("No API blueprint available")

# Global error handler for serverless
@app.errorhandler(Exception)
def handle_exception(e):
    """Handle unexpected exceptions in serverless environment"""
    logging.error(f"Unhandled exception: {str(e)}")
    return jsonify({
        'error': 'Internal server error',
        'message': 'Something went wrong processing your request'
    }), 500

# Web routes
@app.route('/')
def index():
    """Main page with API testing interface"""
    try:
        return render_template('index.html')
    except Exception as e:
        logging.error(f"Template error: {e}")
        return jsonify({
            'service': 'yt-dlp API (Vercel)',
            'status': 'running',
            'message': 'Template not found, but API is available',
            'api_endpoints': [
                '/api/health',
                '/api/platforms', 
                '/api/info',
                '/api/formats',
                '/api/download'
            ]
        })

@app.route('/docs')
def docs():
    """API documentation page"""
    try:
        return render_template('docs.html')
    except Exception as e:
        logging.error(f"Documentation template error: {e}")
        return jsonify({
            'documentation': 'Template not found',
            'api_info': 'Visit /api/health for API status',
            'endpoints': {
                'GET /api/health': 'Service health check',
                'GET /api/platforms': 'Supported platforms',
                'POST /api/info': 'Get video metadata',
                'POST /api/formats': 'Get available formats',
                'POST /api/download': 'Download video'
            }
        })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Page not found',
        'available_routes': ['/', '/docs', '/api/health']
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'service': 'yt-dlp API (Vercel)'
    }), 500

# Vercel entry point
if __name__ == '__main__':
    # For local development
    app.run(host='0.0.0.0', port=5000, debug=False)