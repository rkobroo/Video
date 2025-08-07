"""
Alternative TikTok video extractor for when yt-dlp fails
This provides fallback methods for TikTok video extraction
"""
import requests
import re
import json
import logging
from urllib.parse import urlparse, parse_qs

logger = logging.getLogger(__name__)

class TikTokExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://www.tiktok.com/',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })

    def extract_video_id(self, url):
        """Extract TikTok video ID from URL"""
        try:
            # Handle different TikTok URL formats
            patterns = [
                r'tiktok\.com/@[^/]+/video/(\d+)',
                r'tiktok\.com/.*?video/(\d+)',
                r'vm\.tiktok\.com/(\w+)',
                r'vt\.tiktok\.com/(\w+)'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, url)
                if match:
                    return match.group(1)
            
            return None
        except Exception as e:
            logger.error(f"Error extracting TikTok video ID: {e}")
            return None

    def get_video_info(self, url):
        """
        Get basic video information using alternative methods
        This is a fallback when yt-dlp fails
        """
        try:
            video_id = self.extract_video_id(url)
            if not video_id:
                return None
            
            # Return basic info that can be constructed
            return {
                'title': f'TikTok Video {video_id}',
                'video_id': video_id,
                'platform': 'TikTok',
                'webpage_url': url,
                'note': 'Limited info available - TikTok extraction currently restricted'
            }
            
        except Exception as e:
            logger.error(f"TikTok fallback extraction failed: {e}")
            return None

def is_tiktok_url(url):
    """Check if URL is a TikTok URL"""
    tiktok_domains = ['tiktok.com', 'vm.tiktok.com', 'vt.tiktok.com']
    try:
        parsed_url = urlparse(url)
        return any(domain in parsed_url.netloc for domain in tiktok_domains)
    except:
        return False