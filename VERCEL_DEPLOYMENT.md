# Vercel Deployment Guide

## Overview

This yt-dlp API has been optimized for Vercel deployment with specific adaptations to work within serverless constraints.

## Key Vercel Optimizations

### 1. **Serverless Function Limits**
- Maximum execution time: 60 seconds (configurable in vercel.json)
- Memory limit: 1024MB (default)
- File system: Read-only except /tmp directory

### 2. **Code Adaptations**
- **Direct URL Response**: Instead of downloading files, the API returns direct video URLs for large files
- **Timeout Protection**: Reduced socket timeouts and connection limits
- **Memory Optimization**: Smaller chunk sizes and limited concurrent downloads
- **Format Filtering**: Only serves videos under 720p and 50MB for direct download

### 3. **File Structure for Vercel**
```
├── vercel.json         # Vercel configuration
├── main.py            # Auto-detects Vercel environment
├── app_vercel.py      # Vercel-optimized Flask app
├── api_vercel.py      # Vercel-optimized API endpoints
├── requirements.txt   # Python dependencies (auto-generated)
└── templates/         # Web interface templates
```

## Deployment Steps

### 1. **Prepare for Vercel**
1. Install Vercel CLI: `npm i -g vercel`
2. Login: `vercel login`
3. Clone this project to your local machine

### 2. **Deploy to Vercel**
```bash
# Navigate to project directory
cd your-project

# Deploy with Vercel
vercel

# Follow the prompts:
# - Link to existing project? No
# - Project name: your-api-name
# - Directory: ./
# - Framework: Other
```

### 3. **Environment Variables**
Set these in your Vercel dashboard:
```
FLASK_ENV=production
SESSION_SECRET=your-random-secret-key
```

### 4. **Custom Domain (Optional)**
- Go to Vercel Dashboard → Your Project → Settings → Domains
- Add your custom domain

## API Behavior on Vercel

### Download Endpoint Differences
On Vercel, the `/api/download` endpoint behaves differently:

**Short Videos (< 10 minutes, < 50MB):**
- Returns direct video URL for streaming/download
- No server-side file handling

**Long Videos (> 10 minutes):**
- Returns error with suggestion to use direct URL
- Provides direct video URL in response

**Example Response:**
```json
{
  "success": true,
  "title": "Video Title",
  "direct_url": "https://direct-video-url.com/video.mp4",
  "format": "720p",
  "filesize": 25000000,
  "note": "Direct video URL provided for Vercel compatibility"
}
```

## Limitations on Vercel

### 1. **File Size Limits**
- Videos larger than 50MB return direct URLs instead of downloads
- No server-side file storage

### 2. **Execution Time**
- 60-second timeout for all operations
- Long videos may timeout during processing

### 3. **Dependencies**
- ffmpeg not available (uses yt-dlp's built-in capabilities only)
- Limited to formats that don't require post-processing

## Monitoring and Debugging

### 1. **Vercel Function Logs**
- Access logs in Vercel Dashboard → Functions tab
- Monitor execution time and memory usage

### 2. **Error Handling**
- All errors return JSON responses
- Detailed error messages for debugging

### 3. **Health Check**
```bash
curl https://your-app.vercel.app/api/health
```

## Performance Tips

### 1. **Format Selection**
- Use `best[height<=720]` for faster processing
- Avoid `best` format for large videos

### 2. **URL Validation**
- Validate URLs client-side when possible
- Use shorter video URLs for better performance

### 3. **Caching**
- Vercel automatically caches static responses
- API responses are not cached by default

## Troubleshooting

### Common Issues:

1. **Timeout Errors**
   - Reduce video quality in request
   - Try shorter videos first

2. **Memory Errors**
   - Use format selectors with file size limits
   - Example: `best[filesize<50M]`

3. **Dependencies Missing**
   - Ensure all imports are available in Vercel environment
   - Check requirements.txt is properly configured

### Support Matrix:

| Platform | Direct Download | Stream URL | Info/Metadata |
|----------|----------------|------------|---------------|
| YouTube | ✅ (< 50MB) | ✅ | ✅ |
| TikTok | ✅ | ✅ | ✅ |
| Instagram | ✅ | ✅ | ✅ |
| Twitter | ✅ | ✅ | ✅ |
| Facebook | ⚠️ (Limited) | ✅ | ✅ |
| Vimeo | ✅ | ✅ | ✅ |
| Dailymotion | ✅ | ✅ | ✅ |
| Twitch | ⚠️ (Limited) | ✅ | ✅ |

✅ = Full support  
⚠️ = Limited support due to platform restrictions