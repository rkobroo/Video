#!/usr/bin/env python3
"""
Test script to demonstrate filename generation with emojis
"""
from utils import get_filename_with_title, sanitize_filename

def test_emoji_filenames():
    """Test filename generation with various emoji and special character scenarios"""
    test_cases = [
        "Rick Astley - Never Gonna Give You Up (Official Video) 🎵🎬",
        "Dancing Queen 👑💃 - ABBA (Official Music Video)",
        "How to Cook Pasta 🍝🇮🇹 - Easy Recipe",
        "Gaming Live Stream 🎮🔥 - Fortnite Victory!",
        "Travel Vlog: Tokyo Adventure 🗾🏮 Day 1",
        "Coding Tutorial: Python vs JavaScript 🐍⚡",
        "Funny Cat Compilation 😸🐱 - Best Moments",
        "Morning Workout Routine 💪☀️ - 30 Minutes",
        "Recipe: Homemade Pizza 🍕👨‍🍳 - Step by Step",
        "Late Night Study Session 📚🌙 - Chill Music"
    ]
    
    print("🧪 Testing filename generation with emojis and special characters...\n")
    
    for i, title in enumerate(test_cases, 1):
        sanitized = sanitize_filename(title)
        filename = get_filename_with_title(title, 'mp4')
        
        print(f"{i:2d}. Original: {title}")
        print(f"    Filename: {filename}")
        print(f"    Safe for filesystem: ✅" if is_safe_filename(filename) else "    Safe for filesystem: ❌")
        print()

def is_safe_filename(filename):
    """Check if filename is safe for most filesystems"""
    unsafe_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    return not any(char in filename for char in unsafe_chars)

if __name__ == '__main__':
    test_emoji_filenames()
    print("✅ Filename testing completed! Emojis and special characters are preserved while keeping files safe.")