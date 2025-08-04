# Social Media Video Downloader API

A powerful Flask-based REST API that downloads videos from multiple social media platforms using yt-dlp. Features comprehensive platform support, emoji-preserving filenames, and both Replit and Vercel deployment compatibility.

## ✨ Features

- **Multi-Platform Support**: YouTube, TikTok, Instagram, Twitter/X, Facebook, Vimeo, Dailymotion, Twitch
- **Emoji-Friendly Filenames**: Preserves full video titles with emojis and special characters
- **Flexible Quality Options**: Choose from best, 1080p, 720p, 480p, worst, or audio-only
- **Serverless Ready**: Optimized for both traditional hosting and serverless platforms
- **Unlimited Downloads**: No rate limiting for maximum performance
- **Smart Error Handling**: Platform-specific fallback strategies

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd social-media-downloader-api
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the server**
   ```bash
   python main.py
   ```

4. **Test the API**
   ```bash
   curl -X POST http://localhost:5000/api/info \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
   ```

### Replit Deployment

1. Import this repository to Replit
2. The app will automatically start with the configured workflow
3. Access your API at `https://<your-repl-name>.<your-username>.replit.app`

### Vercel Deployment

1. **Deploy to Vercel**
   ```bash
   vercel --prod
   ```

2. **Configure environment** (if needed)
   - The app automatically detects Vercel environment
   - Uses optimized serverless configuration

## 📚 API Documentation

### Endpoints

#### `GET /api/health`
Check API status and version.

#### `POST /api/info`
Get video metadata without downloading.

```json
{
  "url": "https://www.tiktok.com/@user/video/123456"
}
```

#### `POST /api/download`
Download video with specified quality.

```json
{
  "url": "https://www.tiktok.com/@user/video/123456",
  "format": "best"
}
```

### Supported Formats
- `best` - Highest available quality
- `1080p` - 1080p resolution
- `720p` - 720p resolution  
- `480p` - 480p resolution
- `worst` - Lowest available quality
- `audio` - Audio only

## 🎯 Platform Support

| Platform | Status | Notes |
|----------|--------|-------|
| YouTube | ✅ Full | All formats, playlists, live streams |
| TikTok | ✅ Full | Public videos, emoji filenames |
| Instagram | ✅ Full | Posts, reels, stories (public) |
| Twitter/X | ✅ Full | Video tweets, optimized format |
| Facebook | ✅ Full | Public videos, fb.watch links |
| Vimeo | ✅ Full | All video types |
| Dailymotion | ✅ Full | All formats |
| Twitch | ✅ Full | VODs, clips |

## 🔧 Configuration

### Environment Variables

- `SESSION_SECRET` - Flask session secret key
- `DATABASE_URL` - PostgreSQL database URL (optional)

### Deployment-Specific Features

#### Replit
- Traditional Flask application with full feature set
- File downloads with preserved filenames
- Comprehensive error logging

#### Vercel
- Serverless-optimized with 60-second timeout
- Returns direct video URLs for large files
- Memory-efficient processing

## 📋 Requirements

- Python 3.8+
- Flask 2.0+
- yt-dlp (latest)
- Dependencies listed in `pyproject.toml`

## 🛠️ Development

### Project Structure
```
├── api.py              # Main API routes and logic
├── api_vercel.py       # Vercel-optimized API version
├── app.py              # Flask application setup
├── app_vercel.py       # Vercel-optimized app
├── main.py             # Entry point with auto-detection
├── utils.py            # Utility functions
├── routes.py           # Web interface routes
├── templates/          # HTML templates
├── static/            # Static assets
├── vercel.json        # Vercel configuration
└── docs/              # Documentation files
```

### Adding New Platforms

1. Update `get_format_for_url()` in `utils.py`
2. Add platform-specific configuration in API files
3. Test with platform URLs
4. Update documentation

## 🎨 Features Showcase

### Emoji Filename Preservation
```
Original: "Next kis pa bnao 🤌......./... comment karo ...../ ❤️‍🩹"
Filename: "Next kis pa bnao 🤌......._... comment karo ....._ ❤️‍🩹.mp4"
```

### Smart Format Selection
- **TikTok**: `best[ext=mp4]/mp4/best`
- **Facebook**: `best[ext=mp4]/best`
- **Instagram**: `best[ext=mp4]/best`
- **Twitter**: `best[ext=mp4]/best`

## 🔒 Usage Guidelines

### Best Practices
- Use public video URLs for best compatibility
- Respect platform terms of service
- Consider rate limiting for production use
- Monitor file storage usage

### Limitations
- Private content requires authentication cookies
- Some platforms may block automated access
- File size limits apply on serverless platforms

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. Please respect the terms of service of supported platforms.

## 🆘 Support

For issues and questions:
1. Check the [Platform Support Guide](PLATFORM_SUPPORT.md)
2. Review the [Vercel Deployment Guide](VERCEL_DEPLOYMENT.md)
3. Open an issue on GitHub

---

**Built with ❤️ using Flask and yt-dlp**# VideoHarvest
# VideoHarvest
