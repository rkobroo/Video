# Platform Support Guide

## Supported Platforms

Your yt-dlp API now supports all major social media platforms with optimized configurations:

### ✅ Fully Supported Platforms

| Platform | Status | Notes |
|----------|--------|-------|
| **YouTube** | ✅ Full Support | All formats, playlists, live streams |
| **TikTok** | ✅ Full Support | Public videos, optimized MP4 format |
| **Instagram** | ✅ Full Support | Posts, reels, stories (public) |
| **Twitter/X** | ✅ Full Support | Video tweets, optimized format |
| **Facebook** | ✅ Full Support | Public videos, optimized format |
| **Vimeo** | ✅ Full Support | All video types |
| **Dailymotion** | ✅ Full Support | All video formats |
| **Twitch** | ✅ Full Support | VODs, clips |

## Platform-Specific Optimizations

### TikTok
- **Format**: Automatically uses `best[ext=mp4]/mp4/best`
- **Filename**: Preserves full title with emojis (e.g., "Next kis pa bnao 🤌...❤️‍🩹...")
- **Requirements**: Public videos only (no login required)

### Facebook
- **Format**: Optimized for MP4 output
- **Compatibility**: Works with fb.watch and facebook.com links
- **Requirements**: Public videos

### Instagram
- **Format**: MP4 optimized for best compatibility
- **Support**: Posts, Reels, IGTV
- **Requirements**: Public content only

### Twitter/X
- **Format**: MP4 optimized
- **Support**: Video tweets from both twitter.com and x.com domains

## Emoji & Special Character Support

### Filename Features
- **Full Unicode Support**: Preserves all emojis and special characters
- **Smart Truncation**: Maintains readability while staying within filesystem limits
- **Safe Characters**: Automatically replaces problematic characters (/, :, etc.) with underscores

### Example Filenames
```
Original: "Next kis pa bnao 🤌......./... comment karo ...../ ❤️‍🩹"
Filename: "Next kis pa bnao 🤌......._... comment karo ....._ ❤️‍🩹.mp4"

Original: "Gaming Stream 🎮🔥 - Epic Victory! 🏆"
Filename: "Gaming Stream 🎮🔥 - Epic Victory! 🏆.mp4"
```

## Troubleshooting

### Common Issues

#### TikTok: "Requested format is not available"
- **Solution**: Use default format selection (API handles this automatically)
- **Cause**: Platform changed available formats
- **Fix**: API now uses fallback format selection

#### Facebook: "Private video" errors
- **Solution**: Ensure video is public or shared with public visibility
- **Note**: Private videos require authentication cookies

#### Instagram: "Login required"
- **Solution**: Use public posts only
- **Alternative**: Stories and private posts need authentication

### Error Handling
The API now includes improved error messages:
- **Format errors**: Automatic fallback to compatible formats
- **Access errors**: Clear instructions for public content requirements
- **Network errors**: Retry logic with platform-specific timeouts

## Best Practices

### URL Types That Work Best
1. **Direct video URLs** (highest success rate)
2. **Public posts** (no login required)
3. **Shared links** (properly formatted)

### URL Types to Avoid
1. **Private content** (requires authentication)
2. **Age-restricted content** (may need cookies)
3. **Geo-blocked content** (region restrictions)

## API Usage Examples

### Download with Full Title
```bash
curl -X POST http://your-api.com/api/download \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.tiktok.com/@user/video/123456",
    "format": "best"
  }'
```

### Get Video Info with Emojis
```bash
curl -X POST http://your-api.com/api/info \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.tiktok.com/@user/video/123456"
  }'
```

## Recent Improvements

### Version 2.0 Features
- ✅ **Emoji Preservation**: Full Unicode support in filenames
- ✅ **Platform Optimization**: Specific format selection per platform
- ✅ **Better Error Handling**: Clear messages for platform-specific issues
- ✅ **Extended Title Support**: Preserves long titles with hashtags
- ✅ **Vercel Compatibility**: Serverless-optimized for deployment

### Filename Length Handling
- **Maximum**: 255 characters (filesystem standard)
- **Smart Truncation**: Word-boundary aware
- **Emoji Preservation**: Never truncates in middle of emoji sequences
- **Extension Handling**: Automatically appends correct file extension