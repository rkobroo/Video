import os
import re
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

def validate_url(url):
    """Validate if the provided string is a valid URL"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def cleanup_file(file_path):
    """Safely remove a file"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Cleaned up file: {file_path}")
    except Exception as e:
        logger.error(f"Failed to cleanup file {file_path}: {str(e)}")

def get_supported_formats():
    """Return list of commonly supported format selectors"""
    return [
        {
            'name': 'Best Quality',
            'selector': 'best',
            'description': 'Highest quality available'
        },
        {
            'name': 'Best 1080p',
            'selector': 'best[height<=1080]',
            'description': 'Best quality up to 1080p'
        },
        {
            'name': 'Best 720p',
            'selector': 'best[height<=720]',
            'description': 'Best quality up to 720p'
        },
        {
            'name': 'Best 480p',
            'selector': 'best[height<=480]',
            'description': 'Best quality up to 480p'
        },
        {
            'name': 'Worst Quality',
            'selector': 'worst',
            'description': 'Lowest quality available'
        },
        {
            'name': 'Audio Only',
            'selector': 'bestaudio',
            'description': 'Best audio quality only'
        }
    ]

def sanitize_filename(filename):
    """Sanitize filename while preserving emojis and special characters"""
    import unicodedata
    
    # Only remove characters that are problematic for file systems
    # Keep emojis and unicode characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Replace multiple spaces with single space
    filename = re.sub(r'\s+', ' ', filename)
    
    # Remove leading/trailing whitespace and dots
    filename = filename.strip(' .')
    
    # If filename is empty after cleaning, provide default
    if not filename:
        filename = 'video'
    
    # Increase length limit and preserve more of the title
    if len(filename) > 255:  # Most filesystems support 255 characters
        # Try to cut at word boundary
        words = filename.split()
        truncated = ''
        for word in words:
            if len(truncated + ' ' + word) <= 250:  # Leave room for extension
                truncated = truncated + ' ' + word if truncated else word
            else:
                break
        filename = truncated if truncated else filename[:250]
    
    return filename

def get_filename_with_title(title, ext='mp4'):
    """Generate filename from video title preserving emojis"""
    sanitized_title = sanitize_filename(title)
    return f"{sanitized_title}.{ext}"
import re
import os
import tempfile
import unicodedata

def validate_url(url):
    """Validate if the provided URL is a valid format"""
    if not url or not isinstance(url, str):
        return False
    
    # Basic URL validation
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return url_pattern.match(url) is not None

def cleanup_file(file_path):
    """Safely remove a file if it exists"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            # Also try to remove the directory if it's empty
            try:
                parent_dir = os.path.dirname(file_path)
                if parent_dir and parent_dir != tempfile.gettempdir():
                    os.rmdir(parent_dir)
            except OSError:
                pass  # Directory not empty or other error
    except Exception as e:
        print(f"Error cleaning up file {file_path}: {e}")

def get_supported_formats():
    """Return a list of commonly supported video formats"""
    return [
        {'id': 'best', 'description': 'Best quality available'},
        {'id': 'best[height<=1080]', 'description': 'Best quality up to 1080p'},
        {'id': 'best[height<=720]', 'description': 'Best quality up to 720p'},
        {'id': 'best[height<=480]', 'description': 'Best quality up to 480p'},
        {'id': 'worst', 'description': 'Lowest quality available'},
        {'id': 'bestaudio', 'description': 'Audio only (best quality)'}
    ]

def get_filename_with_title(title, ext):
    """
    Generate a safe filename from video title, preserving emojis and unicode characters
    while replacing problematic characters for filesystems
    """
    if not title:
        return f"video.{ext}"
    
    # Replace problematic characters for filesystems but preserve emojis
    # Characters that cause issues: / \ : * ? " < > |
    problematic_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    
    safe_title = title
    for char in problematic_chars:
        safe_title = safe_title.replace(char, '_')
    
    # Remove any leading/trailing whitespace and dots
    safe_title = safe_title.strip(' .')
    
    # Limit length to avoid filesystem issues (keeping some buffer for extension)
    max_length = 200
    if len(safe_title) > max_length:
        safe_title = safe_title[:max_length].rstrip(' .')
    
    # Ensure we have a valid filename
    if not safe_title or safe_title.isspace():
        safe_title = "video"
    
    return f"{safe_title}.{ext}"

def sanitize_filename(filename):
    """
    Sanitize filename for cross-platform compatibility while preserving unicode
    """
    if not filename:
        return "file"
    
    # Normalize unicode characters
    filename = unicodedata.normalize('NFC', filename)
    
    # Replace problematic characters
    problematic_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for char in problematic_chars:
        filename = filename.replace(char, '_')
    
    # Remove control characters but keep printable unicode
    filename = ''.join(char for char in filename if unicodedata.category(char)[0] != 'C')
    
    # Trim and ensure it's not empty
    filename = filename.strip(' .')
    if not filename:
        filename = "file"
    
    return filename
