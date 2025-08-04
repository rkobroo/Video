
"""
Main entry point for the yt-dlp API
Supports both Replit and Vercel deployments
"""
import os

# Check if running on Vercel
if os.environ.get('VERCEL') or os.environ.get('VERCEL_ENV'):
    # Use Vercel-optimized app
    try:
        from app_vercel import app
    except ImportError:
        # Fallback to regular app
        from app import app
else:
    # Use regular app for Replit/other platforms
    from app import app

# Vercel serverless function entry point
app = app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
