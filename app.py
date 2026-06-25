from flask import Flask, render_template, request, jsonify, Response, abort
import os
import requests
import yt_dlp
import urllib.parse

# Cookie file for YouTube authentication
COOKIE_FILE = os.environ.get('COOKIE_FILE', '/app/cookies.txt')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_info', methods=['POST'])
def fetch_info():
    """Fetch video info without downloading"""
    data = request.json
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'socket_timeout': 10,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            # Spoof iOS client — bypasses YouTube bot detection on server IPs
            'extractor_args': {'youtube': {'player_client': ['ios']}},
        }
        
        # Add cookie file if it exists
        if os.path.exists(COOKIE_FILE):
            ydl_opts['cookiefile'] = COOKIE_FILE
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        
        # We don't strictly enforce file sizes anymore since it's streamed, 
        # but we can return it for the UI preview
        filesize = int(info.get('filesize') or info.get('filesize_approx') or 0)
        
        return jsonify({
            'title': info.get('title', 'Unknown'),
            'duration': info.get('duration', 0),
            'thumbnail': info.get('thumbnail', ''),
            'filesize': filesize,
            'format': info.get('format', 'Unknown'),
            'ext': info.get('ext', 'mp4'),
        })
    except Exception as e:
        return jsonify({'error': str(e)[:200]}), 400


@app.route('/stream', methods=['GET'])
def stream():
    """Proxy stream the video directly to the client"""
    url = request.args.get('url')
    if not url:
        abort(400, "URL required")
        
    try:
        ydl_opts = {
            # Force a pre-merged format (video+audio in one file) since we stream directly
            'format': 'best[ext=mp4]/best',
            'quiet': True,
            'no_warnings': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'extractor_args': {'youtube': {'player_client': ['ios']}},
        }
        
        if os.path.exists(COOKIE_FILE):
            ydl_opts['cookiefile'] = COOKIE_FILE
            
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
        download_url = info.get('url')
        if not download_url:
            # Sometimes YouTube extraction fails to get a direct URL
            abort(400, "Could not extract direct stream URL")
            
        title = info.get('title', 'video')
        ext = info.get('ext', 'mp4')
        
        # Strip invalid characters from filename
        safe_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
        filename = f"{safe_title}.{ext}"
        
        # Secure filename for headers
        filename_encoded = urllib.parse.quote(filename)

        # Open stream to the video provider
        req = requests.get(download_url, stream=True, headers={'User-Agent': ydl_opts['user_agent']})
        
        def generate():
            # Stream in 1MB chunks to keep RAM usage extremely low
            for chunk in req.iter_content(chunk_size=1024*1024):
                if chunk:
                    yield chunk
                
        headers = {
            'Content-Disposition': f"attachment; filename*=UTF-8''{filename_encoded}",
            'Content-Type': req.headers.get('content-type', 'video/mp4')
        }
        
        # Pass the content-length so the browser knows the total download size
        if 'content-length' in req.headers:
            headers['Content-Length'] = req.headers['content-length']
            
        return Response(generate(), headers=headers)
        
    except Exception as e:
        print(f"Streaming error: {e}")
        abort(500, f"Failed to stream video: {str(e)[:200]}")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
