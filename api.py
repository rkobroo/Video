import os
import tempfile
import json
import yt_dlp
from flask import Blueprint, request, jsonify, send_file
from werkzeug.exceptions import BadRequest
import logging
from utils import validate_url, cleanup_file, get_supported_formats
from app import limiter

logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__)

# Supported platforms
SUPPORTED_PLATFORMS = [
    'youtube.com', 'youtu.be', 'tiktok.com', 'instagram.com', 
    'twitter.com', 'x.com', 'facebook.com', 'vimeo.com',
    'dailymotion.com', 'twitch.tv'
]

@api_bp.route('/info', methods=['POST'])
def get_video_info():
    """Get video metadata without downloading"""
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400
        
        url = data['url'].strip()
        if not validate_url(url):
            return jsonify({'error': 'Invalid URL format'}), 400
        
        # Configure yt-dlp options for info extraction only
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                
                # Extract relevant metadata
                metadata = {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration'),
                    'uploader': info.get('uploader', 'Unknown'),
                    'upload_date': info.get('upload_date'),
                    'view_count': info.get('view_count'),
                    'thumbnail': info.get('thumbnail'),
                    'description': info.get('description', ''),
                    'platform': info.get('extractor_key', 'Unknown'),
                    'formats_available': len(info.get('formats', [])),
                    'webpage_url': info.get('webpage_url', url)
                }
                
                return jsonify({
                    'success': True,
                    'metadata': metadata,
                    'supported_formats': get_supported_formats()
                })
                
            except yt_dlp.DownloadError as e:
                logger.error(f"yt-dlp download error: {str(e)}")
                return jsonify({'error': f'Failed to extract video info: {str(e)}'}), 400
            except Exception as e:
                logger.error(f"Unexpected error during info extraction: {str(e)}")
                return jsonify({'error': 'Unable to process this URL'}), 500
                
    except Exception as e:
        logger.error(f"Error in get_video_info: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/download', methods=['POST'])
def download_video():
    """Download video with specified options"""
    temp_file = None
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400
        
        url = data['url'].strip()
        if not validate_url(url):
            return jsonify({'error': 'Invalid URL format'}), 400
        
        # Parse options
        format_selector = data.get('format', 'best[height<=720]')
        audio_only = data.get('audio_only', False)
        
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        
        # Configure yt-dlp options with emoji support
        ydl_opts = {
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'restrictfilenames': False,  # Allow unicode characters and emojis
            'ignoreerrors': False,  # Don't ignore errors, handle them properly
            'writesubtitles': False,
            'writeautomaticsub': False,
            'no_check_certificate': True,  # Help with some platform issues
            'extractor_args': {
                'tiktok': {
                    'webpage_url_domain': 'tiktok.com'
                }
            }
        }
        
        if audio_only:
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        else:
            # Improved format selection for different platforms
            if 'tiktok.com' in url.lower():
                # TikTok specific format handling
                ydl_opts['format'] = 'best[ext=mp4]/mp4/best'
            elif 'facebook.com' in url.lower() or 'fb.watch' in url.lower():
                # Facebook format handling
                ydl_opts['format'] = 'best[ext=mp4]/mp4/best'
            elif 'instagram.com' in url.lower():
                # Instagram format handling
                ydl_opts['format'] = 'best[ext=mp4]/mp4/best'
            elif 'twitter.com' in url.lower() or 'x.com' in url.lower():
                # Twitter/X format handling
                ydl_opts['format'] = 'best[ext=mp4]/mp4/best'
            else:
                # For YouTube and other platforms, use user selection
                ydl_opts['format'] = format_selector
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                # Extract info first
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'video')
                ext = info.get('ext', 'mp4')
                
                # Generate filename with title (including emojis)
                from utils import get_filename_with_title
                desired_filename = get_filename_with_title(title, ext)
                
                # Download the video
                ydl.download([url])
                
                # Find the downloaded file
                files = os.listdir(temp_dir)
                if not files:
                    return jsonify({'error': 'Download completed but no file found'}), 500
                
                temp_file = os.path.join(temp_dir, files[0])
                
                # Get file info
                file_size = os.path.getsize(temp_file)
                
                # Use the sanitized title as download filename
                return send_file(
                    temp_file,
                    as_attachment=True,
                    download_name=desired_filename,  # Use title-based filename
                    mimetype='application/octet-stream'
                )
                
            except yt_dlp.DownloadError as e:
                logger.error(f"yt-dlp download error: {str(e)}")
                return jsonify({'error': f'Download failed: {str(e)}'}), 400
            except Exception as e:
                logger.error(f"Unexpected error during download: {str(e)}")
                return jsonify({'error': 'Download failed due to server error'}), 500
                
    except Exception as e:
        logger.error(f"Error in download_video: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        # Cleanup temporary files
        if temp_file and os.path.exists(temp_file):
            cleanup_file(temp_file)

@api_bp.route('/formats', methods=['POST'])
def get_available_formats():
    """Get available formats for a video"""
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400
        
        url = data['url'].strip()
        if not validate_url(url):
            return jsonify({'error': 'Invalid URL format'}), 400
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'listformats': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                formats = []
                
                for fmt in info.get('formats', []):
                    format_info = {
                        'format_id': fmt.get('format_id'),
                        'ext': fmt.get('ext'),
                        'resolution': fmt.get('resolution', 'audio only' if fmt.get('vcodec') == 'none' else 'unknown'),
                        'filesize': fmt.get('filesize'),
                        'fps': fmt.get('fps'),
                        'vcodec': fmt.get('vcodec'),
                        'acodec': fmt.get('acodec'),
                        'format_note': fmt.get('format_note', '')
                    }
                    formats.append(format_info)
                
                return jsonify({
                    'success': True,
                    'formats': formats,
                    'title': info.get('title', 'Unknown')
                })
                
            except yt_dlp.DownloadError as e:
                logger.error(f"yt-dlp error: {str(e)}")
                return jsonify({'error': f'Failed to get formats: {str(e)}'}), 400
                
    except Exception as e:
        logger.error(f"Error in get_available_formats: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/supported-platforms')
def supported_platforms():
    """Get list of supported platforms"""
    return jsonify({
        'success': True,
        'platforms': SUPPORTED_PLATFORMS,
        'total': len(SUPPORTED_PLATFORMS)
    })

@api_bp.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'yt-dlp API',
        'version': '1.0.0'
    })
