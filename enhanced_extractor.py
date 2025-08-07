
"""
Enhanced video extractor with multiple fallback methods
Specifically designed to handle problematic platforms like TikTok
"""
import logging
import yt_dlp
from tikwm_extractor import TikWMExtractor, is_tiktok_url
from advanced_tiktok_extractor import extract_tiktok_with_fallback

logger = logging.getLogger(__name__)

class EnhancedExtractor:
    def __init__(self):
        self.tikwm = TikWMExtractor()
    
    def extract_info(self, url, download=False):
        """Enhanced extraction with multiple fallback methods"""
        
        if is_tiktok_url(url):
            return self._extract_tiktok_enhanced(url, download)
        else:
            return self._extract_standard(url, download)
    
    def _extract_tiktok_enhanced(self, url, download=False):
        """Enhanced TikTok extraction with multiple methods"""
        methods = [
            ("TikWM API", self._method_tikwm),
            ("yt-dlp (updated)", self._method_yt_dlp_updated),
            ("yt-dlp (mobile)", self._method_yt_dlp_mobile),
            ("yt-dlp (desktop)", self._method_yt_dlp_desktop),
            ("Advanced extractor", self._method_advanced_extractor)
        ]
        
        for method_name, method_func in methods:
            try:
                logger.info(f"Trying TikTok extraction method: {method_name}")
                result = method_func(url, download)
                if result:
                    logger.info(f"TikTok extraction successful with: {method_name}")
                    return result
            except Exception as e:
                logger.warning(f"Method {method_name} failed: {str(e)}")
                continue
        
        logger.error("All TikTok extraction methods failed")
        return None
    
    def _method_tikwm(self, url, download=False):
        """TikWM API method"""
        return self.tikwm.get_video_info(url)
    
    def _method_yt_dlp_updated(self, url, download=False):
        """Updated yt-dlp method with latest options"""
        opts = {
            'quiet': True,
            'no_warnings': True,
            'user_agent': 'TikTok 34.1.2 rv:341102 (iPhone; iOS 17.0; en_US) Cronet',
            'http_headers': {
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Referer': 'https://www.tiktok.com/',
                'X-Requested-With': 'XMLHttpRequest',
            },
            'extractor_args': {
                'tiktok': {
                    'api_hostname': 'api16-normal-c-useast1a.tiktokv.com',
                    'app_version': '34.1.2',
                    'build_number': '341102'
                }
            },
            'socket_timeout': 30,
            'retries': 5
        }
        
        with yt_dlp.YoutubeDL(opts) as ydl:
            return ydl.extract_info(url, download=download)
    
    def _method_yt_dlp_mobile(self, url, download=False):
        """Mobile yt-dlp method"""
        opts = {
            'quiet': True,
            'user_agent': 'com.zhiliaoapp.musically/2023600040 (Linux; U; Android 13; en_US; Pixel 7; Build/TD1A.220804.031; Cronet/102.0.5005.125)',
            'http_headers': {
                'X-Argus': 'null',
                'X-Ladon': 'null',
            },
            'socket_timeout': 30
        }
        
        with yt_dlp.YoutubeDL(opts) as ydl:
            return ydl.extract_info(url, download=download)
    
    def _method_yt_dlp_desktop(self, url, download=False):
        """Desktop yt-dlp method"""
        opts = {
            'quiet': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'http_headers': {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': 'https://www.tiktok.com/',
            },
            'socket_timeout': 30
        }
        
        with yt_dlp.YoutubeDL(opts) as ydl:
            return ydl.extract_info(url, download=download)
    
    def _method_advanced_extractor(self, url, download=False):
        """Advanced extractor method"""
        return extract_tiktok_with_fallback(url)
    
    def _extract_standard(self, url, download=False):
        """Standard extraction for non-TikTok platforms"""
        opts = {
            'quiet': True,
            'no_warnings': True,
            'socket_timeout': 60,
            'retries': 3
        }
        
        with yt_dlp.YoutubeDL(opts) as ydl:
            return ydl.extract_info(url, download=download)
