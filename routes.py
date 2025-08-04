from flask import render_template
from app import app

@app.route('/')
def index():
    """Main page with API testing interface"""
    return render_template('index.html')

@app.route('/docs')
def api_docs():
    """API documentation page"""
    return render_template('docs.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('index.html'), 500
