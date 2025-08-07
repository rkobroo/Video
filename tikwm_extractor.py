
"""
TikWM.com API integration for TikTok video downloads
This provides a reliable alternative to yt-dlp for TikTok content
"""
import requests
import logging
import re
import json
from urllib.parse import urlparse, parse_qs, quote

logger = logging.getLogger(__name__)

class TikWMExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.tikwm.com/',
            'Origin': 'https://www.tikwm.com'
        })
        
        # Multiple API endpoints for better reliability
        self.api_endpoints = [
            'https://www.tikwm.com/api/',
            'https://api.tikwm.com/api/',
            'https://tikwm.com/api/',
            'https://tikwm.online/api/',
            'https://api16.tikwm.com/api/'
        ]
        
        # Additional TikTok download APIs as fallbacks
        self.fallback_apis = [
            {
                'name': 'SaveTT',
                'url': 'https://savett.cc/api/ajaxSearch',
                'method': self._extract_with_savett
            },
            {
                'name': 'SnapTik',
                'url': 'https://snaptik.app/abc2.php',
                'method': self._extract_with_snaptik
            },
            {
                'name': 'TikMate',
                'url': 'https://tikmate.online/download',
                'method': self._extract_with_tikmate
            }
        ]

    def resolve_tiktok_url(self, url):
        """Resolve shortened TikTok URLs to full URLs"""
        try:
            # Handle different TikTok URL formats
            if 'vm.tiktok.com' in url or 'vt.tiktok.com' in url:
                logger.info(f"Resolving shortened TikTok URL: {url}")
                response = self.session.head(url, allow_redirects=True, timeout=10)
                resolved_url = response.url
                logger.info(f"Resolved URL: {url} -> {resolved_url}")
                
                # Check if the resolved URL is valid (not a 404 page)
                if 'notfound' in resolved_url or response.status_code == 404:
                    logger.warning(f"TikTok URL may be invalid or video not found: {url} -> {resolved_url}")
                    return url  # Return original URL to try anyway
                
                return resolved_url
            return url
        except Exception as e:
            logger.error(f"Error resolving TikTok URL {url}: {e}")
            return url

    def get_video_info(self, url):
        """Get TikTok video information using multiple methods"""
        try:
            resolved_url = self.resolve_tiktok_url(url)
            
            # Try TikWM API with resolved URL first
            info = self._extract_with_tikwm(resolved_url)
            if info:
                return info
            
            # If resolved URL failed and it's different from original, try original
            if resolved_url != url:
                logger.info("Trying original URL after resolved URL failed")
                info = self._extract_with_tikwm(url)
                if info:
                    return info
            
            # Try fallback APIs with both URLs
            for api in self.fallback_apis:
                for test_url in [resolved_url, url]:
                    try:
                        logger.info(f"Trying fallback API: {api['name']} with URL: {test_url}")
                        info = api['method'](test_url)
                        if info:
                            logger.info(f"Successfully extracted with {api['name']}")
                            return info
                    except Exception as e:
                        logger.warning(f"Fallback API {api['name']} failed with {test_url}: {e}")
                        continue
            
            return None
            
        except Exception as e:
            logger.error(f"Error in get_video_info: {e}")
            return None

    def _extract_with_tikwm(self, url):
        """Extract using TikWM API with multiple endpoints"""
        for endpoint in self.api_endpoints:
            try:
                logger.info(f"Requesting TikWM API for resolved URL: {url}")
                
                params = {
                    'url': url,
                    'count': 12,
                    'cursor': 0,
                    'web': 1,
                    'hd': 1
                }
                
                # Add specific headers for this request
                headers = {
                    'Accept': 'application/json, text/plain, */*',
                    'Accept-Encoding': 'identity',  # Avoid compression issues
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Referer': 'https://www.tikwm.com/',
                }
                
                response = self.session.get(endpoint, params=params, headers=headers, timeout=15)
                response.raise_for_status()
                
                # Check content type first
                content_type = response.headers.get('content-type', '').lower()
                if 'application/json' not in content_type:
                    logger.error(f"TikWM API returned non-JSON content type: {content_type}")
                    continue
                
                # Check if response is valid JSON
                try:
                    data = response.json()
                except json.JSONDecodeError:
                    logger.error(f"TikWM API returned invalid JSON for URL {url}: {response.text[:100]}")
                    continue
                
                if data.get('code') == 0 and data.get('data'):
                    video_data = data['data']
                    
                    # Extract video information
                    info = {
                        'title': video_data.get('title', 'TikTok Video'),
                        'uploader': video_data.get('author', {}).get('unique_id', 'Unknown'),
                        'duration': video_data.get('duration'),
                        'view_count': video_data.get('play_count'),
                        'like_count': video_data.get('digg_count'),
                        'comment_count': video_data.get('comment_count'),
                        'share_count': video_data.get('share_count'),
                        'upload_date': video_data.get('create_time'),
                        'thumbnail': video_data.get('cover'),
                        'description': video_data.get('title', ''),
                        'webpage_url': url,
                        'platform': 'TikTok',
                        'formats': []
                    }
                    
                    # Helper function to fix URLs
                    def fix_url(url_path):
                        if not url_path:
                            return None
                        if url_path.startswith('http'):
                            return url_path
                        elif url_path.startswith('/'):
                            return f'https://www.tikwm.com{url_path}'
                        else:
                            return f'https://www.tikwm.com/{url_path}'
                    
                    # Add available formats with proper URLs
                    if video_data.get('hdplay'):
                        fixed_url = fix_url(video_data['hdplay'])
                        if fixed_url:
                            info['formats'].append({
                                'format_id': 'hd',
                                'url': fixed_url,
                                'quality': 'HD',
                                'ext': 'mp4'
                            })
                    
                    if video_data.get('play'):
                        fixed_url = fix_url(video_data['play'])
                        if fixed_url:
                            info['formats'].append({
                                'format_id': 'sd',
                                'url': fixed_url,
                                'quality': 'SD',
                                'ext': 'mp4'
                            })
                    
                    if video_data.get('wmplay'):
                        fixed_url = fix_url(video_data['wmplay'])
                        if fixed_url:
                            info['formats'].append({
                                'format_id': 'watermark',
                                'url': fixed_url,
                                'quality': 'SD (with watermark)',
                                'ext': 'mp4'
                            })
                    
                    if video_data.get('music'):
                        fixed_url = fix_url(video_data['music'])
                        if fixed_url:
                            info['formats'].append({
                                'format_id': 'audio',
                                'url': fixed_url,
                                'quality': 'Audio',
                                'ext': 'mp3'
                            })
                    
                    # Fix thumbnail URL as well
                    if video_data.get('cover'):
                        info['thumbnail'] = fix_url(video_data['cover'])
                    
                    logger.info(f"Successfully extracted TikTok info using TikWM: {info['title']}")
                    return info
                else:
                    logger.warning(f"TikWM API returned error for {url}: {data}")
                    continue
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"TikWM API request failed for endpoint {endpoint}: {e}")
                continue
            except Exception as e:
                logger.error(f"Unexpected error with TikWM API endpoint {endpoint}: {e}")
                continue
        
        return None

    def _extract_with_snaptik(self, url):
        """Extract using SnapTik API as fallback"""
        try:
            data = {
                'url': url,
                'token': '',
                'lang': 'en'
            }
            
            response = self.session.post(
                'https://snaptik.app/abc2.php',
                data=data,
                timeout=15
            )
            
            if response.status_code == 200 and 'download' in response.text.lower():
                # Basic info extraction for SnapTik
                return {
                    'title': 'TikTok Video (SnapTik)',
                    'platform': 'TikTok',
                    'webpage_url': url,
                    'formats': [{
                        'format_id': 'snaptik_sd',
                        'quality': 'SD',
                        'ext': 'mp4'
                    }],
                    'note': 'Extracted using SnapTik fallback'
                }
        except Exception as e:
            logger.error(f"SnapTik extraction failed: {e}")
        
        return None

    def _extract_with_tikmate(self, url):
        """Extract using TikMate API as fallback"""
        try:
            data = {'url': url}
            
            response = self.session.post(
                'https://tikmate.online/download',
                data=data,
                timeout=15
            )
            
            if response.status_code == 200:
                # Try to parse response for actual download URLs
                response_text = response.text
                
                # Look for video URLs in the response
                import re
                video_urls = re.findall(r'href="([^"]*\.mp4[^"]*)"', response_text)
                
                formats = []
                if video_urls:
                    for i, video_url in enumerate(video_urls[:3]):  # Limit to 3 formats
                        formats.append({
                            'format_id': f'tikmate_{i}',
                            'url': video_url,
                            'quality': 'SD',
                            'ext': 'mp4'
                        })
                else:
                    # Fallback format without actual URL
                    formats.append({
                        'format_id': 'tikmate_sd',
                        'url': '',  # Empty URL to avoid KeyError
                        'quality': 'SD',
                        'ext': 'mp4'
                    })
                
                return {
                    'title': 'TikTok Video (TikMate)',
                    'platform': 'TikTok',
                    'webpage_url': url,
                    'formats': formats,
                    'note': 'Extracted using TikMate fallback'
                }
        except Exception as e:
            logger.error(f"TikMate extraction failed: {e}")
        
        return None

    def _extract_with_savett(self, url):
        """Extract using SaveTT API as fallback"""
        try:
            data = {
                'q': url,
                'lang': 'en'
            }
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = self.session.post(
                'https://savett.cc/api/ajaxSearch',
                data=data,
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get('status') == 'ok' and result.get('data'):
                        video_data = result['data']
                        
                        formats = []
                        # Look for video links
                        if video_data.get('video_hd'):
                            formats.append({
                                'format_id': 'hd',
                                'url': video_data['video_hd'],
                                'quality': 'HD',
                                'ext': 'mp4'
                            })
                        
                        if video_data.get('video'):
                            formats.append({
                                'format_id': 'sd',
                                'url': video_data['video'],
                                'quality': 'SD',
                                'ext': 'mp4'
                            })
                        
                        if video_data.get('audio'):
                            formats.append({
                                'format_id': 'audio',
                                'url': video_data['audio'],
                                'quality': 'Audio',
                                'ext': 'mp3'
                            })
                        
                        return {
                            'title': video_data.get('title', 'TikTok Video (SaveTT)'),
                            'uploader': video_data.get('author', 'Unknown'),
                            'thumbnail': video_data.get('cover'),
                            'platform': 'TikTok',
                            'webpage_url': url,
                            'formats': formats,
                            'note': 'Extracted using SaveTT fallback'
                        }
                except json.JSONDecodeError:
                    pass
                    
        except Exception as e:
            logger.error(f"SaveTT extraction failed: {e}")
        
        return None

def is_tiktok_url(url):
    """Check if URL is a TikTok URL"""
    tiktok_domains = ['tiktok.com', 'vm.tiktok.com', 'vt.tiktok.com']
    try:
        parsed_url = urlparse(url)
        return any(domain in parsed_url.netloc for domain in tiktok_domains)
    except:
        return False
