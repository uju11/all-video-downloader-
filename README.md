# Simple Video Downloader Web App

## Architecture

- **Framework**: Flask (WSGI)
- **Concurrency Model**:
  - Main Flask server runs on `threaded=True` to handle multiple HTTP requests
  - `ProcessPoolExecutor` with `max_workers=5` manages up to 5 simultaneous video downloads
  - Each download runs in a separate process (avoids GIL, true parallelism)
- **Frontend**: Single-page HTML/JavaScript
- **Storage**: Downloads saved to `downloads/` folder

## Run Locally

1. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

2. Start the app:

```powershell
python app.py
```

3. Open http://localhost:5000 in your browser.

## Run with Docker

1. Build and start:

```bash
docker-compose up --build
```

2. Open http://localhost:5000 in your browser.

3. Stop the container:

```bash
docker-compose down
```

### Notes
- Downloads persist in the local `./downloads/` folder (mounted as a volume)
- App listens on port 5000 inside and outside the container
- `ffmpeg` is pre-installed in the container (needed by yt-dlp for some formats)
