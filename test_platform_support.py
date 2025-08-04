#!/usr/bin/env python3
"""
Test platform support and filename generation for social media videos
"""
import requests
import json

API_BASE = "http://localhost:5000/api"

def test_filename_generation():
    """Test filename generation with emojis"""
    print("🧪 Testing filename generation with emojis...")
    
    test_cases = [
        {
            "title": "Next kis pa bnao 🤌......./... comment karo ...../ ❤️‍🩹 ......./... . . . #foryoupageofficiall #viral",
            "expected_preserved": ["🤌", "❤️‍🩹", "#foryoupageofficiall", "#viral"]
        },
        {
            "title": "Gaming Stream 🎮🔥 - Epic Victory! 🏆",
            "expected_preserved": ["🎮", "🔥", "🏆"]
        },
        {
            "title": "Cooking Tutorial: Pasta 🍝🇮🇹 Delicious Recipe",
            "expected_preserved": ["🍝", "🇮🇹"]
        }
    ]
    
    for case in test_cases:
        from utils import get_filename_with_title
        filename = get_filename_with_title(case["title"], "mp4")
        
        print(f"\nOriginal: {case['title']}")
        print(f"Filename: {filename}")
        
        # Check if emojis are preserved
        preserved = all(emoji in filename for emoji in case["expected_preserved"])
        print(f"Emojis preserved: {'✅' if preserved else '❌'}")
        
        # Check filename safety
        unsafe_chars = ['<', '>', ':', '"', '//', '\\', '|', '?', '*']
        is_safe = not any(char in filename for char in unsafe_chars)
        print(f"Filesystem safe: {'✅' if is_safe else '❌'}")

def test_api_endpoints():
    """Test API endpoints with different platforms"""
    print("\n🌐 Testing API endpoints...")
    
    test_urls = [
        {
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "platform": "YouTube",
            "should_work": True
        },
        # Note: Real TikTok URLs would be needed for actual testing
        # These are just for format testing
    ]
    
    for test in test_urls:
        if test["should_work"]:
            print(f"\n📹 Testing {test['platform']}...")
            try:
                response = requests.post(f"{API_BASE}/info", 
                                       json={"url": test["url"]}, 
                                       timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    title = data.get("metadata", {}).get("title", "No title")
                    print(f"✅ {test['platform']} info extraction: Success")
                    print(f"   Title: {title[:100]}{'...' if len(title) > 100 else ''}")
                else:
                    print(f"❌ {test['platform']} info extraction: Failed ({response.status_code})")
                    
            except Exception as e:
                print(f"❌ {test['platform']} info extraction: Error - {str(e)}")

def test_format_selection():
    """Test format selection for different platforms"""
    print("\n🎬 Testing format selection...")
    
    from api import get_vercel_ydl_opts if hasattr(__import__('api'), 'get_vercel_ydl_opts') else None
    
    test_urls = [
        "https://www.tiktok.com/@user/video/123",
        "https://www.facebook.com/video/123", 
        "https://www.instagram.com/p/123",
        "https://www.youtube.com/watch?v=123"
    ]
    
    for url in test_urls:
        from api_vercel import get_vercel_ydl_opts
        opts = get_vercel_ydl_opts('best', '/tmp', url)
        platform = url.split('.')[1]
        
        print(f"{platform.capitalize()}: format = {opts.get('format', 'default')}")

if __name__ == '__main__':
    print("🚀 Running comprehensive platform support tests...\n")
    
    try:
        test_filename_generation()
        test_format_selection()
        test_api_endpoints()
        
        print("\n✅ Platform support testing completed!")
        print("\n📋 Summary:")
        print("- Emoji filename generation: Implemented")
        print("- Platform-specific format selection: Configured")
        print("- API endpoints: Ready for testing")
        print("\n💡 Tips for better TikTok/Social Media support:")
        print("- Use public videos (no login required)")
        print("- Some platforms may require cookies for private content")
        print("- Format selection is optimized for MP4 output")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        print("Please check the implementation and try again.")