# Social Media Video Downloader API

## Overview

A Flask-based REST API service that enables video downloading from multiple social media platforms including YouTube, TikTok, Instagram, Twitter, Facebook, Vimeo, Dailymotion, and Twitch. The application leverages yt-dlp for video extraction and provides a web interface for API testing alongside comprehensive documentation. **Now optimized for both Replit and Vercel deployment with serverless compatibility.**

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask with Blueprint-based modular architecture
- **API Design**: RESTful endpoints with JSON request/response format
- **Rate Limiting**: Unlimited access (rate limiting disabled per user request)
- **Error Handling**: Centralized error handling with proper HTTP status codes
- **Logging**: Structured logging throughout the application for debugging and monitoring

### Video Processing Engine
- **Core Library**: yt-dlp for video extraction and metadata retrieval
- **Supported Platforms**: YouTube, TikTok, Instagram, Twitter/X, Facebook, Vimeo, Dailymotion, Twitch
- **Format Selection**: Configurable quality options (best, 1080p, 720p, 480p, worst, audio-only)
- **Smart Filename Generation**: Preserves full video titles with emojis and special characters (up to 255 chars)
- **Platform-Specific Format Selection**: Optimized format handling for TikTok, Facebook, Instagram, and Twitter
- **Temporary File Management**: Secure handling of downloaded files with automatic cleanup

### Frontend Architecture
- **UI Framework**: Bootstrap 5 with dark theme
- **JavaScript**: Vanilla ES6 for API interactions and DOM manipulation
- **Template Engine**: Jinja2 templates for server-side rendering
- **User Interface**: Single-page application with API testing interface and documentation

### Security and Validation
- **URL Validation**: Server-side URL format and safety validation
- **Input Sanitization**: Request data validation and sanitization
- **Rate Limiting**: Multiple-tier rate limiting to prevent abuse
- **Proxy Support**: ProxyFix middleware for proper header handling behind reverse proxies

### Application Structure
- **Modular Design**: Blueprint-based separation of API and web routes
- **Configuration Management**: Environment-based configuration with sensible defaults
- **Error Pages**: Custom 404/500 error handling with fallback to main interface
- **Deployment Flexibility**: Auto-detection of deployment environment (Replit vs Vercel)

### Vercel Serverless Compatibility
- **Optimized Entry Point**: `main.py` automatically detects Vercel environment
- **Serverless Adaptations**: Memory-optimized yt-dlp configuration with 60-second timeout limits
- **Direct URL Strategy**: Returns video URLs for large files instead of server-side downloads
- **Error Handling**: Comprehensive serverless-specific error responses
- **File Management**: Temporary file handling optimized for serverless constraints

## External Dependencies

### Core Libraries
- **Flask**: Web framework for API and route handling
- **yt-dlp**: Video extraction library supporting multiple platforms
- **Flask-Limiter**: Rate limiting implementation
- **Werkzeug**: WSGI utilities and proxy handling

### Frontend Dependencies
- **Bootstrap 5**: UI framework with dark theme
- **Font Awesome 6**: Icon library for user interface elements

### Runtime Environment
- **Python**: Primary runtime environment
- **WSGI**: Standard Python web server interface
- **Temporary File System**: OS-level temporary directory management for downloaded content

### Platform Integrations
- **YouTube**: Video and metadata extraction
- **TikTok**: Short-form video downloading
- **Instagram**: Social media content extraction
- **Twitter/X**: Tweet video downloading
- **Facebook**: Social video content
- **Vimeo**: Professional video platform
- **Dailymotion**: Video sharing platform
- **Twitch**: Live streaming and VOD content
