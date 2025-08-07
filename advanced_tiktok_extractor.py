"""
Advanced TikTok extractor using multiple methods
This handles TikTok's evolving anti-bot measures
"""
import json
import re
import requests
import logging
from urllib.parse import urlparse, parse_qs
import yt_dlp

logger = logging.getLogger(__name__)

class AdvancedTikTokExtractor:
    def __init__(self):
        self.session = requests.Session()
        # Use multiple user agents to avoid detection
        self.user_agents = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
        ]
        
    def get_enhanced_yt_dlp_options(self, url):
        """Get enhanced yt-dlp options with latest TikTok workarounds"""
        return {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'no_check_certificate': True,
            'ignoreerrors': True,
            'user_agent': 'TikTok 26.1.3 rv:261103 (iPhone; iOS 14.0; en_US) Cronet',
            'http_headers': {
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Origin': 'https://www.tiktok.com',
                'Referer': 'https://www.tiktok.com/',
                'Sec-Fetch-Site': 'same-site',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'X-Requested-With': 'XMLHttpRequest',
            },
            'extractor_args': {
                'tiktok': {
                    'api_hostname': 'api16-normal-c-useast1a.tiktokv.com',
                    'app_version': '26.1.3',
                    'build_number': '261103',
                    'manifest_app_version': '2611',
                    'device_id': '7318518857994389254',
                    'install_id': '7318518740146652166'
                }
            },
            'socket_timeout': 30,
            'retries': 10,
            'fragment_retries': 10,
            'skip_unavailable_fragments': True,
        }

    def extract_with_multiple_methods(self, url):
        """Try multiple extraction methods for TikTok"""
        methods = [
            self._method_enhanced_yt_dlp,
            self._method_alternative_yt_dlp,
            self._method_mobile_yt_dlp,
        ]
        
        for i, method in enumerate(methods, 1):
            try:
                logger.info(f"Trying TikTok extraction method {i}")
                result = method(url)
                if result:
                    logger.info(f"TikTok extraction successful with method {i}")
                    return result
            except Exception as e:
                logger.warning(f"Method {i} failed: {str(e)}")
                continue
        
        return None

    def _method_enhanced_yt_dlp(self, url):
        """Enhanced yt-dlp method with latest options"""
        opts = self.get_enhanced_yt_dlp_options(url)
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info

    def _method_alternative_yt_dlp(self, url):
        """Alternative yt-dlp configuration"""
        opts = {
            'quiet': True,
            'no_warnings': True,
            'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
            'http_headers': {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': 'https://www.tiktok.com/',
            },
            'extractor_args': {
                'tiktok': {
                    'api_hostname': 'api19-normal-c-useast1a.tiktokv.com',
                }
            }
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info

    def _method_mobile_yt_dlp(self, url):
        """Mobile-focused yt-dlp method"""
        opts = {
            'quiet': True,
            'user_agent': 'com.zhiliaoapp.musically/2023600040 (Linux; U; Android 10; en_US; Pixel 4; Build/QQ3A.200805.001; Cronet/58.0.2991.0)',
            'http_headers': {
                'X-Argus': 'null',
                'X-Ladon': 'null',  
            }
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info

def extract_tiktok_with_fallback(url):
    """Main function to extract TikTok with multiple fallback methods"""
    extractor = AdvancedTikTokExtractor()
    return extractor.extract_with_multiple_methods(url)