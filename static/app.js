// API base URL
const API_BASE = '/api';

// DOM elements
const videoForm = document.getElementById('videoForm');
const videoUrlInput = document.getElementById('videoUrl');
const formatSelect = document.getElementById('formatSelect');
const audioOnlyCheckbox = document.getElementById('audioOnly');
const getInfoBtn = document.getElementById('getInfoBtn');
const getFormatsBtn = document.getElementById('getFormatsBtn');
const resultsSection = document.getElementById('resultsSection');
const loadingSpinner = document.getElementById('loadingSpinner');
const resultsContent = document.getElementById('resultsContent');
const platformsList = document.getElementById('platformsList');

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    loadSupportedPlatforms();
    
    // Event listeners
    videoForm.addEventListener('submit', handleDownload);
    getInfoBtn.addEventListener('click', handleGetInfo);
    getFormatsBtn.addEventListener('click', handleGetFormats);
    audioOnlyCheckbox.addEventListener('change', handleAudioOnlyChange);
});

// Handle audio only checkbox change
function handleAudioOnlyChange() {
    if (audioOnlyCheckbox.checked) {
        formatSelect.value = 'bestaudio';
        formatSelect.disabled = true;
    } else {
        formatSelect.disabled = false;
        formatSelect.value = 'best[height<=720]';
    }
}

// Show loading state
function showLoading() {
    resultsSection.classList.remove('d-none');
    loadingSpinner.classList.remove('d-none');
    resultsContent.innerHTML = '';
}

// Hide loading state
function hideLoading() {
    loadingSpinner.classList.add('d-none');
}

// Show error message
function showError(message) {
    hideLoading();
    resultsContent.innerHTML = `
        <div class="alert alert-danger" role="alert">
            <i class="fas fa-exclamation-triangle me-2"></i>
            <strong>Error:</strong> ${message}
        </div>
    `;
}

// Show success message
function showSuccess(title, content) {
    hideLoading();
    resultsContent.innerHTML = `
        <div class="alert alert-success" role="alert">
            <i class="fas fa-check-circle me-2"></i>
            <strong>${title}</strong>
        </div>
        ${content}
    `;
}

// Get video info
async function handleGetInfo() {
    const url = videoUrlInput.value.trim();
    if (!url) {
        showError('Please enter a video URL');
        return;
    }

    showLoading();

    try {
        const response = await fetch(`${API_BASE}/info`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to get video info');
        }

        const metadata = data.metadata;
        const duration = metadata.duration ? formatDuration(metadata.duration) : 'Unknown';
        const viewCount = metadata.view_count ? formatNumber(metadata.view_count) : 'Unknown';
        const uploadDate = metadata.upload_date ? formatDate(metadata.upload_date) : 'Unknown';

        const content = `
            <div class="row">
                <div class="col-md-4">
                    ${metadata.thumbnail ? `<img src="${metadata.thumbnail}" class="img-fluid rounded" alt="Thumbnail">` : ''}
                </div>
                <div class="col-md-8">
                    <h5>${metadata.title}</h5>
                    <p class="text-muted mb-1"><i class="fas fa-user me-1"></i> ${metadata.uploader}</p>
                    <p class="text-muted mb-1"><i class="fas fa-calendar me-1"></i> ${uploadDate}</p>
                    <p class="text-muted mb-1"><i class="fas fa-clock me-1"></i> ${duration}</p>
                    <p class="text-muted mb-1"><i class="fas fa-eye me-1"></i> ${viewCount} views</p>
                    <p class="text-muted mb-1"><i class="fas fa-globe me-1"></i> ${metadata.platform}</p>
                    <p class="text-muted"><i class="fas fa-film me-1"></i> ${metadata.formats_available} formats available</p>
                    ${metadata.description ? `<p class="mt-2"><small>${metadata.description.substring(0, 200)}${metadata.description.length > 200 ? '...' : ''}</small></p>` : ''}
                </div>
            </div>
        `;

        showSuccess('Video Information Retrieved', content);

    } catch (error) {
        showError(error.message);
    }
}

// Get available formats
async function handleGetFormats() {
    const url = videoUrlInput.value.trim();
    if (!url) {
        showError('Please enter a video URL');
        return;
    }

    showLoading();

    try {
        const response = await fetch(`${API_BASE}/formats`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to get formats');
        }

        let tableRows = '';
        data.formats.forEach(format => {
            const fileSize = format.filesize ? formatBytes(format.filesize) : 'Unknown';
            const fps = format.fps || 'N/A';
            tableRows += `
                <tr>
                    <td>${format.format_id}</td>
                    <td>${format.ext}</td>
                    <td>${format.resolution}</td>
                    <td>${fileSize}</td>
                    <td>${fps}</td>
                    <td>${format.format_note}</td>
                </tr>
            `;
        });

        const content = `
            <h6>Available formats for: ${data.title}</h6>
            <div class="table-responsive">
                <table class="table table-striped table-sm">
                    <thead>
                        <tr>
                            <th>Format ID</th>
                            <th>Extension</th>
                            <th>Resolution</th>
                            <th>File Size</th>
                            <th>FPS</th>
                            <th>Note</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${tableRows}
                    </tbody>
                </table>
            </div>
        `;

        showSuccess('Available Formats', content);

    } catch (error) {
        showError(error.message);
    }
}

// Handle download
async function handleDownload(event) {
    event.preventDefault();
    
    const url = videoUrlInput.value.trim();
    if (!url) {
        showError('Please enter a video URL');
        return;
    }

    showLoading();

    try {
        const requestBody = {
            url: url,
            format: formatSelect.value,
            audio_only: audioOnlyCheckbox.checked
        };

        const response = await fetch(`${API_BASE}/download`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Download failed');
        }

        // Handle file download
        const blob = await response.blob();
        const contentDisposition = response.headers.get('Content-Disposition');
        let filename = 'video';
        
        if (contentDisposition) {
            const filenameMatch = contentDisposition.match(/filename="(.+)"/);
            if (filenameMatch) {
                filename = filenameMatch[1];
            }
        }

        // Create download link
        const downloadUrl = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(downloadUrl);
        document.body.removeChild(a);

        showSuccess('Download Started', `
            <p>Your download should start automatically. If it doesn't, please check your browser's download settings.</p>
            <p><strong>Filename:</strong> ${filename}</p>
        `);

    } catch (error) {
        showError(error.message);
    }
}

// Load supported platforms
async function loadSupportedPlatforms() {
    try {
        const response = await fetch(`${API_BASE}/supported-platforms`);
        const data = await response.json();

        if (data.success) {
            let platformsHtml = '';
            data.platforms.forEach(platform => {
                platformsHtml += `
                    <div class="col-md-3 col-sm-4 col-6 mb-2">
                        <span class="badge bg-secondary">${platform}</span>
                    </div>
                `;
            });
            platformsList.innerHTML = platformsHtml;
        }
    } catch (error) {
        platformsList.innerHTML = '<div class="col-12"><p class="text-muted">Unable to load platforms</p></div>';
    }
}

// Utility functions
function formatDuration(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    if (hours > 0) {
        return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
}

function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    }
    if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function formatDate(dateString) {
    if (!dateString || dateString.length !== 8) return 'Unknown';
    const year = dateString.substring(0, 4);
    const month = dateString.substring(4, 6);
    const day = dateString.substring(6, 8);
    return `${year}-${month}-${day}`;
}
