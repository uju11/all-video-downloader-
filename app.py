from flask import Flask, render_template, request, jsonify, send_from_directory, abort
import os
import uuid
from concurrent.futures import ThreadPoolExecutor
import threading
import json
import time
import signal
from contextlib import contextmanager

DOWNLOAD_DIR = "/app/downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

app = Flask(__name__)

# Executor for downloads (threads) - allow up to 5 concurrent downloads
executor = ThreadPoolExecutor(max_workers=5)

# Track tasks and futures
tasks = {}
future_to_task = {}
cancelled_tasks = set()  # Track cancelled tasks for cleanup
tasks_lock = threading.Lock()
TASKS_FILE = os.path.join(os.path.dirname(__file__), 'tasks.json')
DOWNLOAD_TIMEOUT = 3600  # 1 hour timeout per download

# Load persisted tasks on startup
def load_tasks():
    global tasks
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, 'r') as f:
                tasks = json.load(f)
        except:
            tasks = {}

# Save tasks to file
def save_tasks():
    try:
        with open(TASKS_FILE, 'w') as f:
            json.dump(tasks, f)
    except:
        pass

load_tasks()


def download_worker(url, out_dir, task_id=None):
    # This function runs in a separate process
    import yt_dlp
    import os

    try:
        ydl_opts = {
            'outtmpl': os.path.join(out_dir, '%(title)s [%(id)s].%(ext)s'),
            'quiet': False,
            'no_warnings': False,
            'socket_timeout': 30,
            'http_chunk_size': 10485760,  # 10MB chunks for faster download
            'progress_hooks': [lambda d: _progress_hook(d, task_id)] if task_id else [],
        }
        
        with tasks_lock:
            if task_id and task_id in tasks:
                tasks[task_id]['status'] = 'running'
                tasks[task_id]['started'] = time.time()
                save_tasks()
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

        title = info.get('title') or info.get('id')
        video_id = info.get('id')

        # Find the actual file that was downloaded (might have different extension due to merging)
        filename = None
        filepath = None
        for f in os.listdir(out_dir):
            # Match by video_id since title may have encoding issues
            if f"[{video_id}]" in f:
                filename = f
                filepath = os.path.join(out_dir, filename)
                break

        if not filename or not os.path.exists(filepath):
            # Fallback to constructed filename
            ext = info.get('ext') or 'mp4'
            filename = f"{title} [{video_id}].{ext}"
            filepath = os.path.join(out_dir, filename)

        file_size = os.path.getsize(filepath) if os.path.exists(filepath) else 0
        
        with tasks_lock:
            if task_id and task_id in tasks:
                tasks[task_id]['status'] = 'completed'
                tasks[task_id]['filename'] = filename
                tasks[task_id]['title'] = title
                tasks[task_id]['progress'] = 100
                tasks[task_id]['size'] = file_size
                tasks[task_id]['completed'] = time.time()
                save_tasks()
        
        return {'status': 'completed', 'filename': filename, 'title': title, 'size': file_size, 'progress': 100}
    
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)[:200]}"
        with tasks_lock:
            if task_id and task_id in tasks:
                tasks[task_id]['status'] = 'error'
                tasks[task_id]['error'] = error_msg
                tasks[task_id]['completed'] = time.time()
                save_tasks()
        return {'status': 'error', 'error': error_msg}

def _progress_hook(d, task_id):
    """Called by yt-dlp during download - updates progress in real-time"""
    if not task_id:
        return
    
    try:
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            downloaded = d.get('downloaded_bytes', 0)
            if total > 0:
                progress = int((downloaded / total) * 100)
                speed = d.get('speed', 0)
                eta = d.get('eta', 0)
                with tasks_lock:
                    if task_id in tasks:
                        tasks[task_id]['progress'] = progress
                        tasks[task_id]['speed'] = speed
                        tasks[task_id]['eta'] = eta
                        save_tasks()
        elif d['status'] == 'finished':
            with tasks_lock:
                if task_id in tasks:
                    tasks[task_id]['progress'] = 100
                    save_tasks()
    except Exception as e:
        print(f"Progress hook error: {e}")


def _on_done(fut):
    """Called when a download thread completes - final cleanup"""
    with tasks_lock:
        task_id = future_to_task.pop(fut, None)
        if not task_id:
            return
        
        # If the download_worker didn't update status, mark as error
        if task_id in tasks and tasks[task_id]['status'] == 'running':
            try:
                result = fut.result(timeout=1)
            except Exception as e:
                tasks[task_id]['status'] = 'error'
                tasks[task_id]['error'] = f"Thread exception: {str(e)[:200]}"
                tasks[task_id]['completed'] = time.time()
        
        save_tasks()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/fetch_info', methods=['POST'])
def fetch_info():
    """Fetch video info without downloading"""
    import yt_dlp
    
    data = request.json
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'socket_timeout': 10,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        
        return jsonify({
            'title': info.get('title', 'Unknown'),
            'duration': info.get('duration', 0),
            'thumbnail': info.get('thumbnail', ''),
            'filesize': info.get('filesize') or info.get('filesize_approx', 0),
            'format': info.get('format', 'Unknown'),
            'ext': info.get('ext', 'mp4'),
        })
    except Exception as e:
        return jsonify({'error': str(e)[:200]}), 400


@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json() or {}
    urls = data.get('urls') or []
    created = []
    with tasks_lock:
        for url in urls:
            task_id = uuid.uuid4().hex
            tasks[task_id] = {'url': url, 'status': 'running', 'progress': 0, 'speed': 0, 'eta': 0, 'timestamp': time.time()}
            # submit to executor
            future = executor.submit(download_worker, url, DOWNLOAD_DIR, task_id)
            future_to_task[future] = task_id
            future.add_done_callback(_on_done)
            created.append({'task_id': task_id, 'url': url})
        save_tasks()
    return jsonify({'created': created})


@app.route('/cancel/<task_id>', methods=['POST'])
def cancel_download(task_id):
    """Cancel a download and remove partial file"""
    with tasks_lock:
        if task_id not in tasks:
            return jsonify({'error': 'Task not found'}), 404
        
        task = tasks[task_id]
        if task.get('status') not in ['running', 'queued']:
            return jsonify({'error': 'Cannot cancel completed/cancelled/error task'}), 400
        
        # Mark as cancelled
        cancelled_tasks.add(task_id)
        task['status'] = 'cancelled'
        task['completed'] = time.time()
        
        # Try to delete partial file if it exists
        if task.get('filename'):
            filepath = os.path.join(DOWNLOAD_DIR, task['filename'])
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
            except Exception as e:
                print(f"Could not delete file {filepath}: {e}")
        
        save_tasks()
    
    return jsonify({'status': 'cancelled', 'task_id': task_id})


@app.route('/status', methods=['GET'])
def status():
    with tasks_lock:
        snapshot = {tid: {k: v for k, v in info.items() if k != 'future'} for tid, info in tasks.items()}
    return jsonify(snapshot)


@app.route('/download/<task_id>')
def download_file(task_id):
    with tasks_lock:
        info = tasks.get(task_id)
        if not info:
            print(f"Download failed: Task {task_id} not found")
            abort(404)
        if info.get('status') != 'completed':
            print(f"Download failed: Task {task_id} status is {info.get('status')}, not completed")
            abort(404)
        if not info.get('filename'):
            print(f"Download failed: Task {task_id} has no filename")
            abort(404)
        filename = info['filename']
    # secure: ensure path is inside DOWNLOAD_DIR
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    # If exact filename doesn't exist, try to find by video_id (handles encoding issues)
    if not os.path.exists(filepath):
        print(f"File {filepath} not found, searching by video_id...")
        # Extract video_id from filename pattern: title [video_id].ext
        import re
        match = re.search(r'\[([a-zA-Z0-9_-]+)\]', filename)
        if match:
            video_id = match.group(1)
            for f in os.listdir(DOWNLOAD_DIR):
                if f"[{video_id}]" in f:
                    filename = f
                    filepath = os.path.join(DOWNLOAD_DIR, filename)
                    print(f"Found matching file: {filename}")
                    break

    if not os.path.exists(filepath):
        print(f"Download failed: File {filepath} does not exist")
        abort(404)
    return send_from_directory(DOWNLOAD_DIR, filename, as_attachment=True)


@app.route('/clear_all', methods=['POST'])
def clear_all_downloads():
    """Clear all completed, error, and cancelled downloads, but keep running ones"""
    with tasks_lock:
        to_remove = []
        for task_id, task in tasks.items():
            if task.get('status') in ['completed', 'error', 'cancelled']:
                to_remove.append(task_id)
        
        for task_id in to_remove:
            del tasks[task_id]
        
        save_tasks()
    
    return jsonify({'status': 'cleared', 'removed_count': len(to_remove)})


@app.route('/remove/<task_id>', methods=['POST'])
def remove_task(task_id):
    """Remove a task from the queue (for queued, completed, error, or cancelled tasks)"""
    with tasks_lock:
        if task_id not in tasks:
            return jsonify({'error': 'Task not found'}), 404
        
        task = tasks[task_id]
        if task.get('status') == 'running':
            return jsonify({'error': 'Cannot remove running task. Use cancel instead.'}), 400
        
        # Delete the task
        del tasks[task_id]
        save_tasks()
    
    return jsonify({'status': 'removed', 'task_id': task_id})


@app.route('/restart/<task_id>', methods=['POST'])
def restart_download(task_id):
    """Restart a failed or cancelled download"""
    with tasks_lock:
        if task_id not in tasks:
            return jsonify({'error': 'Task not found'}), 404
        
        task = tasks[task_id]
        if task.get('status') not in ['error', 'cancelled']:
            return jsonify({'error': 'Can only restart error or cancelled tasks'}), 400
        
        url = task['url']
        
        # Reset task status
        task['status'] = 'running'
        task['progress'] = 0
        task['speed'] = 0
        task['eta'] = 0
        task['error'] = None
        task['started'] = time.time()
        task['completed'] = None
        save_tasks()
    
    # Submit to executor
    future = executor.submit(download_worker, url, DOWNLOAD_DIR, task_id)
    with tasks_lock:
        future_to_task[future] = task_id
        future.add_done_callback(_on_done)
    
    return jsonify({'status': 'restarted', 'task_id': task_id})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
