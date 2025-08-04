"""
Vercel-optimized API module for yt-dlp video downloader
This version addresses serverless limitations and timeouts
"""
import os
import tempfile
import logging
from flask import Blueprint, request, jsonify, Response, stream_template
import yt_dlp
from utils import validate_url, cleanup_file, sanitize_filename, get_filename_with_title

logger = logging.getLogger(__name__)

# Create Blueprint for API routes
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Vercel-optimized yt-dlp options
def get_vercel_ydl_opts(format_selector='best', temp_dir=None, url=''):
    """Get yt-dlp options optimized for Vercel serverless environment"""
    if temp_dir is None:
        temp_dir = tempfile.gettempdir()
    
    opts = {
        'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'no_warnings': True,
        'extractaudio': False,
        'audioformat': 'mp3',
        'ignoreerrors': True,
        'no_check_certificate': True,
        'restrictfilenames': False,  # Allow unicode characters and emojis
        # Vercel optimizations
        'concurrent_fragments': 1,  # Reduce memory usage
        'fragment_retries': 1,      # Faster failover
        'socket_timeout': 30,       # Prevent hanging
        'http_chunk_size': 1024*1024,  # 1MB chunks for memory efficiency
        'prefer_free_formats': True,   # Prefer formats that don't require ffmpeg
        'writesubtitles': False,    # Skip subtitles to save time
        'writeautomaticsub': False,
        'youtube_include_dash_manifest': False,  # Skip DASH for speed
    }
    
    # Platform-specific format selection
    if 'tiktok.com' in url.lower():
        opts['format'] = 'best[ext=mp4]/mp4/best'
    elif 'facebook.com' in url.lower() or 'fb.watch' in url.lower():
        opts['format'] = 'best[ext=mp4]/mp4/best'
    elif 'instagram.com' in url.lower():
        opts['format'] = 'best[ext=mp4]/mp4/best'
    elif 'twitter.com' in url.lower() or 'x.com' in url.lower():
        opts['format'] = 'best[ext=mp4]/mp4/best'
    else:
        opts['format'] = format_selector
    
    return opts

def get_supported_platforms():
    """Return list of supported platforms for Vercel deployment"""
    return [
        'YouTube', 'TikTok', 'Instagram', 'Twitter/X', 
        'Facebook', 'Vimeo', 'Dailymotion', 'Twitch'
    ]

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint - optimized for serverless"""
    return jsonify({
        'status': 'healthy',
        'service': 'yt-dlp API (Vercel)',
        'version': '1.0.0',
        'environment': 'serverless'
    })

@api_bp.route('/platforms', methods=['GET'])
def get_platforms():
    """Get supported platforms - cached response"""
    return jsonify({
        'platforms': get_supported_platforms(),
        'total': len(get_supported_platforms())
    })

@api_bp.route('/info', methods=['POST'])
def get_video_info():
    """Get video metadata - optimized for fast response"""
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400
        
        url = data['url']
        if not validate_url(url):
            return jsonify({'error': 'Invalid URL format'}), 400
        
        # Quick info extraction with minimal options
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'socket_timeout': 20,  # Fast timeout for Vercel
            'extract_flat': False,
            'youtube_include_dash_manifest': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                
                # Return essential info only to reduce response time
                response_data = {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration'),
                    'uploader': info.get('uploader'),
                    'view_count': info.get('view_count'),
                    'upload_date': info.get('upload_date'),
                    'description': info.get('description', '')[:500] if info.get('description') else '',  # Truncate description
                    'thumbnail': info.get('thumbnail'),
                    'webpage_url': info.get('webpage_url'),
                    'extractor': info.get('extractor')
                }
                
                return jsonify(response_data)
                
            except Exception as e:
                logger.error(f"yt-dlp extraction error: {str(e)}")
                return jsonify({'error': f'Failed to extract video info: {str(e)}'}), 400
                
    except Exception as e:
        logger.error(f"Video info error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/formats', methods=['POST'])
def get_available_formats():
    """Get available formats - limited for Vercel compatibility"""
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400
        
        url = data['url']
        if not validate_url(url):
            return jsonify({'error': 'Invalid URL format'}), 400
        
        # Fast format detection
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'socket_timeout': 15,
            'listformats': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                formats = info.get('formats', [])
                
                # Filter and simplify formats for Vercel
                simplified_formats = []
                seen_qualities = set()
                
                for fmt in formats:
                    if fmt.get('vcodec') != 'none':  # Video formats only
                        height = fmt.get('height')
                        if height and height not in seen_qualities:
                            simplified_formats.append({
                                'format_id': fmt.get('format_id'),
                                'height': height,
                                'width': fmt.get('width'),
                                'ext': fmt.get('ext'),
                                'filesize': fmt.get('filesize'),
                                'quality': f"{height}p" if height else 'Unknown'
                            })
                            seen_qualities.add(height)
                
                # Sort by quality (highest first)
                simplified_formats.sort(key=lambda x: x.get('height', 0), reverse=True)
                
                return jsonify({
                    'formats': simplified_formats[:10],  # Limit to top 10 formats
                    'total': len(simplified_formats)
                })
                
            except Exception as e:
                logger.error(f"Format extraction error: {str(e)}")
                return jsonify({'error': f'Failed to get formats: {str(e)}'}), 400
                
    except Exception as e:
        logger.error(f"Formats error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/download', methods=['POST'])
def download_video():
    """Download video - with Vercel timeout protection"""
    temp_file = None
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400
        
        url = data['url']
        if not validate_url(url):
            return jsonify({'error': 'Invalid URL format'}), 400
        
        format_selector = data.get('quality', 'best[height<=720]')  # Default to 720p for speed
        
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        
        # Vercel-optimized download options
        ydl_opts = get_vercel_ydl_opts(format_selector, temp_dir, url)
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                # Quick info extraction first
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'video')
                ext = info.get('ext', 'mp4')
                
                # Generate filename with title (including emojis)
                filename_with_title = get_filename_with_title(title, ext)
                
                # Check if video is too long for Vercel (suggest direct link instead)
                duration = info.get('duration')
                if duration and duration > 600:  # 10 minutes
                    return jsonify({
                        'error': 'Video too long for serverless download',
                        'suggestion': 'Use direct video URL',
                        'direct_url': info.get('url'),
                        'title': title,
                        'filename': filename_with_title,
                        'duration': duration
                    }), 400
                
                # For Vercel, return the direct video URL instead of downloading
                # This avoids timeout and storage limitations
                formats = info.get('formats', [])
                if formats:
                    # Find best format within limits
                    suitable_format = None
                    for fmt in formats:
                        if (fmt.get('vcodec') != 'none' and 
                            fmt.get('height', 0) <= 720 and
                            fmt.get('filesize', 0) < 50*1024*1024):  # 50MB limit
                            suitable_format = fmt
                            break
                    
                    if suitable_format:
                        return jsonify({
                            'success': True,
                            'title': title,
                            'filename': filename_with_title,  # Include filename with emojis
                            'direct_url': suitable_format.get('url'),
                            'format': suitable_format.get('format_note', 'Unknown'),
                            'filesize': suitable_format.get('filesize'),
                            'note': 'Direct video URL provided for Vercel compatibility'
                        })
                
                return jsonify({'error': 'No suitable format found for serverless download'}), 400
                
            except Exception as e:
                logger.error(f"Download error: {str(e)}")
                return jsonify({'error': f'Download failed: {str(e)}'}), 400
                
    except Exception as e:
        logger.error(f"Download endpoint error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        # Cleanup
        if temp_file and os.path.exists(temp_file):
            cleanup_file(temp_file)

@api_bp.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@api_bp.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500