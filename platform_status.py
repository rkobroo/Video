"""
Platform status checker to inform users about known issues
"""
import logging

logger = logging.getLogger(__name__)

class PlatformStatus:
    """Track known issues and limitations for different platforms"""
    
    @staticmethod
    def get_platform_status():
        """Get current status of supported platforms"""
        return {
            'youtube': {
                'status': 'operational',
                'features': ['Videos', 'Playlists', 'Live streams'],
                'note': 'Fully supported'
            },
            'tiktok': {
                'status': 'limited',
                'features': ['Basic info extraction'],
                'note': 'TikTok has enhanced anti-bot measures. Video downloading may be restricted.',
                'alternatives': 'Try using other TikTok URLs or download from mobile app'
            },
            'instagram': {
                'status': 'operational',
                'features': ['Posts', 'Reels', 'Stories (public)'],
                'note': 'Public content only'
            },
            'twitter': {
                'status': 'operational',
                'features': ['Video tweets'],
                'note': 'Works with both twitter.com and x.com'
            },
            'facebook': {
                'status': 'operational',
                'features': ['Public videos'],
                'note': 'Public videos only'
            },
            'vimeo': {
                'status': 'operational',
                'features': ['All video types'],
                'note': 'Fully supported'
            },
            'dailymotion': {
                'status': 'operational',
                'features': ['All videos'],
                'note': 'Fully supported'
            },
            'twitch': {
                'status': 'operational',
                'features': ['VODs', 'Clips'],
                'note': 'Fully supported'
            }
        }

    @staticmethod
    def get_platform_recommendations():
        """Get platform-specific recommendations for users"""
        return {
            'tiktok_alternatives': [
                'Try different TikTok URLs from the same creator',
                'Use YouTube if the creator also posts there',
                'Download directly from TikTok mobile app',
                'Check if the video is public and not age-restricted'
            ],
            'general_tips': [
                'Make sure videos are public and not private',
                'Check that URLs are complete and properly formatted',
                'YouTube and Instagram generally have the best success rates',
                'Older videos may work better than very recent ones'
            ]
        }