# Free Deployment Plan for Video Downloader

## App Requirements
- Flask web application
- yt-dlp for video downloading
- FFmpeg for video processing
- Persistent storage for downloaded files
- Network access to external video sites

## Recommended Free Platforms

### Option 1: Render.com (Recommended)
**Pros:**
- Free tier with 512MB RAM
- Supports Docker deployment
- Free persistent disk (up to 1GB)
- Automatic SSL
- Easy deployment from GitHub

**Cons:**
- 512MB RAM may be tight for large downloads
- Free tier spins down after 15min inactivity (cold starts ~30s)
- 1GB storage limit

---

### Option 2: Railway.app
**Pros:**
- Free tier with $5/month credit
- Supports Docker
- Better performance than Render
- Automatic SSL

**Cons:**
- Credit-based system (may run out)
- Less generous free tier than Render
- Storage costs apply

---

### Option 3: Fly.io
**Pros:**
- Free tier with 3 shared CPUs
- Supports Docker
- Global deployment

**Cons:**
- No free persistent storage (paid volumes)
- More complex setup
- Requires credit card for signup

---

### Why Vercel Won't Work
**Vercel is NOT suitable for this app because:**

1. **No Persistent Storage**
   - Vercel's file system is ephemeral (wiped after each deployment)
   - No disk persistence for downloaded files
   - Cannot store files between function invocations

2. **Serverless Limitations**
   - Functions have max execution time (10-60 seconds)
   - Video downloads take much longer
   - Cannot run long-running processes like yt-dlp

3. **No Docker Support**
   - Vercel doesn't support Docker containers
   - Your app requires FFmpeg and system dependencies
   - Cannot install system-level packages

4. **No Background Workers**
   - Cannot run background threads for downloads
   - No support for concurrent processing
   - Functions are stateless and short-lived

**Vercel is designed for:**
- Static websites
- API endpoints (fast responses)
- Serverless functions (under 60s)
- Frontend frameworks (Next.js, React)

**Your app needs:**
- Long-running processes
- Persistent file storage
- System dependencies (FFmpeg)
- Background workers
- Docker containerization

---

## No Credit Card Required Options

### Option A: Self-Hosting (ONLY Option for 5GB+ Without Credit Card)
**Pros:**
- **Unlimited storage** (depends on your hardware)
- No credit card required
- Complete control
- No time limits
- Free forever

**Cons:**
- Requires always-on computer
- Need to handle networking/port forwarding
- You're responsible for maintenance
- Dynamic IP issues (unless using DDNS)

**Hardware Options:**
- **Raspberry Pi 4**: $35-75, 4GB RAM, can add USB storage
- **Old PC/Laptop**: Free if you have one
- **Home server**: Any always-on computer

**Storage:** Unlimited (add external HDD/SSD as needed)
**Cost:** Free (if you have hardware) or one-time hardware purchase
**Credit Card:** Not required

**Verdict:** This is the ONLY option for 5GB+ storage without a credit card

---

### Option B: Cloudflare R2 + Render (Requires Payment Details)
**Note:** Cloudflare now requires payment details for R2 setup, even for free tier.

**Pros:**
- **10GB free storage** (meets your 5GB requirement)
- No egress fees (unique to Cloudflare)
- Simple app hosting on Render

**Cons:**
- **Requires payment details** for Cloudflare account
- More complex architecture (2 services)
- Need to integrate R2 with your app

**Storage:** 10GB free
**Credit Card:** Required for Cloudflare (not for Render)
**Verdict:** Not suitable if you want to avoid payment details entirely

---

### Option C: Render.com (1GB Only, No Credit Card)
**Pros:**
- No credit card required
- Simplest setup
- Automatic SSL
- Easy deployment from GitHub

**Cons:**
- **Only 1GB storage** (below your 5GB requirement)
- Spins down after 15min inactivity
- 512MB RAM limit

**Storage:** 1GB free (not enough for your needs)
**Credit Card:** Not required
**Verdict:** Not suitable for 5GB+ requirement

---

## Platforms with 5GB+ Free Storage

### Option 4: Oracle Cloud Free Tier (Recommended for 5GB+)
**Pros:**
- **200GB free storage** (much more than 5GB)
- True always-on (no spin-down)
- Full VM control
- Docker support
- **No expiry** - free tier lasts forever

**Cons:**
- More complex setup
- **Credit card required for verification** (but no charges)
- ARM architecture (may need adjustments)

**Storage:** 200GB block storage (free forever)
**RAM:** 24GB (2 instances with 12GB each)
**CPU:** 4 OCPU (ARM-based)
**Expiry:** **Never** - free tier is permanent
**Credit Card:** **Required** for verification only (no charges unless you upgrade)

**Important Notes:**
- Credit card is ONLY for identity verification (fraud prevention)
- You will NOT be charged unless you explicitly upgrade to paid services
- Free tier resources are yours to use forever as long as you use them regularly
- Oracle may reclaim resources after 90 days of inactivity, but you can reactivate

---

### Option 5: Cloudflare R2 + Separate Hosting
**Pros:**
- **10GB free storage** (with 10M free egress requests/month)
- S3-compatible API
- No egress fees (unique to Cloudflare)
- Fast global CDN

**Cons:**
- Requires separate hosting for the Flask app
- More complex architecture
- Need to integrate R2 with your app

**Architecture:**
- Host Flask app on Render/Railway (free)
- Store downloads in Cloudflare R2 (10GB free)
- Stream downloads directly from R2

**Implementation:**
```python
# Use boto3 for R2 (S3-compatible)
import boto3

s3 = boto3.client('s3',
    endpoint_url='https://YOUR_ACCOUNT.r2.cloudflarestorage.com',
    aws_access_key_id='YOUR_KEY',
    aws_secret_access_key='YOUR_SECRET'
)

# Upload to R2 instead of local disk
s3.upload_file(filepath, 'video-downloads', filename)
```

---

### Option 6: Backblaze B2 + Separate Hosting
**Pros:**
- **10GB free storage**
- S3-compatible API
- Low cost beyond free tier ($0.005/GB)

**Cons:**
- Egress fees apply (unlike R2)
- Requires separate hosting
- More complex architecture

**Storage:** 10GB free
**Cost after free:** $0.005/GB storage + $0.01/GB download

---

### Option 7: Google Cloud Storage + Cloud Run
**Pros:**
- **5GB free storage**
- Cloud Run free tier (2M requests/month)
- Good integration
- Scalable

**Cons:**
- Egress fees apply
- Free tier has limits
- More complex setup

**Storage:** 5GB free
**Cloud Run:** 2M requests/month free, then pay-per-use

---

### Option 8: AWS Free Tier (12 Months Only)
**Pros:**
- **5GB S3 storage** free for 12 months
- EC2 t2.micro instance free for 12 months
- Reliable and well-documented
- Good performance

**Cons:**
- **Credit card required** for signup
- **Only 12 months free** (not permanent)
- After 12 months, all services are paid
- 1GB RAM on EC2 t2.micro (limited for video processing)
- Egress fees apply after free tier

**Storage:** 5GB S3 free (12 months only)
**Compute:** EC2 t2.micro free (12 months only)
**Credit Card:** Required
**Expiry:** 12 months, then paid

**Verdict:** Not recommended for long-term use. Only suitable for testing or short-term projects.

---

---

## Deployment Instructions

### Option A: Self-Hosting (Step-by-Step)

#### Prerequisites
- Always-on computer (Raspberry Pi, old PC, or home server)
- Docker installed
- Basic networking knowledge

#### Step 1: Prepare Your Hardware
**Option 1: Raspberry Pi 4**
- Purchase Raspberry Pi 4 (4GB RAM recommended)
- Install Raspberry Pi OS Lite
- Add external USB storage for downloads

**Option 2: Old PC/Laptop**
- Install Linux (Ubuntu Server recommended)
- Use existing storage or add external drive

**Option 3: Home Server**
- Use existing always-on computer
- Ensure sufficient storage

#### Step 2: Install Docker
```bash
# On Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Enable Docker
sudo systemctl enable docker
sudo systemctl start docker
```

#### Step 3: Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/video-downloader.git
cd video-downloader
```

#### Step 4: Configure Storage
```bash
# Create downloads directory (or mount external drive)
mkdir -p downloads

# If using external drive, mount it:
sudo mount /dev/sdX1 downloads

# Or update docker-compose.yml to use your storage path
```

#### Step 5: Deploy with Docker
```bash
# Build and run
docker-compose up -d

# Check logs
docker-compose logs -f
```

#### Step 6: Configure Networking

**Option 1: Local Network Only**
```bash
# Access at http://YOUR_LOCAL_IP:5000
# Find your IP:
ip addr show
```

**Option 2: Port Forwarding (Access from Internet)**
1. Log into your router
2. Find port forwarding settings
3. Forward port 5000 to your server's local IP
4. Access at http://YOUR_PUBLIC_IP:5000

**Option 3: Dynamic DNS (for Dynamic IP)**
- Use free DDNS service: duckdns.org, no-ip.com, or freedns.afraid.org
- Install DDNS client on your server
- Access at http://YOUR_DOMAIN.ddns.net:5000

#### Step 7: Add SSL (Optional but Recommended)
```bash
# Install certbot
sudo apt install certbot

# Get certificate (requires port 80)
sudo certbot certonly --standalone -d YOUR_DOMAIN

# Update docker-compose.yml to use SSL
# Add volume: - /etc/letsencrypt:/etc/letsencrypt
# Modify app to use HTTPS
```

#### Step 8: Auto-Start on Boot
```bash
# Docker-compose should auto-start with Docker
# Verify:
sudo systemctl enable docker
```

#### Step 9: Monitor and Maintain
```bash
# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Restart
docker-compose restart

# Update
git pull
docker-compose down
docker-compose up -d --build
```

---

### Option B: Cloudflare R2 + Render (Step-by-Step)

#### Prerequisites
- Cloudflare account (free, no credit card)
- Render account (free, no credit card)
- GitHub account

#### Step 1: Create Cloudflare R2 Bucket
1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com)
2. Navigate to R2 → "Create Bucket"
3. Name: `video-downloads`
4. Click "Create"

#### Step 2: Get R2 API Credentials
1. Go to R2 → "Manage R2 API Tokens"
2. Click "Create API Token"
3. Permissions: Object Read & Write
4. Allow access to: `video-downloads` bucket
5. Save Access Key ID and Secret Access Key

#### Step 3: Get Your R2 Endpoint
1. In Cloudflare Dashboard, go to R2
2. Click on your bucket
3. Find your Account ID in the URL or dashboard
4. Your endpoint will be: `https://<ACCOUNT_ID>.r2.cloudflarestorage.com`

#### Step 4: Code is Already R2-Ready
The app.py has been modified to support R2 automatically via environment variables. No code changes needed!

The app will:
- Download to temporary directory
- Upload to R2 if `USE_R2=true`
- Fall back to local storage if `USE_R2=false`
- Generate presigned URLs for downloads from R2

#### Step 5: Deploy Flask App to Render
1. Push code to GitHub (including updated app.py and requirements.txt)
2. Go to Render.com
3. Create Web Service from GitHub
4. Configure:
   - **Name**: video-downloader
   - **Branch**: main
   - **Runtime**: Docker
5. Add environment variables:
   - `USE_R2`: `true`
   - `R2_ENDPOINT`: Your R2 endpoint URL
   - `R2_ACCESS_KEY`: Your R2 access key
   - `R2_SECRET_KEY`: Your R2 secret key
   - `R2_BUCKET`: `video-downloads`
   - `PORT`: `5000`
6. Click "Create Web Service"

#### Step 6: Verify Deployment
1. Check Render logs for "R2 storage enabled" message
2. Test a video download
3. Verify file appears in your R2 bucket
4. Test download endpoint (should redirect to R2)

#### Step 7: Monitor R2 Usage
1. Go to Cloudflare Dashboard → R2
2. Monitor storage usage (10GB free limit)
3. Monitor egress requests (10M free per month)

**Benefits of this setup:**
- 10GB storage (meets your 5GB requirement)
- No credit card required
- No egress fees (unique to Cloudflare)
- Automatic cleanup after 24 hours
- Presigned URLs for secure downloads

---

### Option 4: Oracle Cloud Free Tier (Step-by-Step)

#### Prerequisites
- Oracle Cloud account (free)
- Credit card for verification (no charges)
- SSH client

#### Step 1: Create Oracle Cloud Account
1. Go to [oracle.com/cloud](https://oracle.com/cloud)
2. Click "Try Free"
3. Sign up with email
4. Verify credit card (required for fraud prevention)
5. Wait for account activation (1-2 hours)

#### Step 2: Create Compute Instance
1. Go to Oracle Cloud Console
2. Navigate to "Compute" → "Instances"
3. Click "Create Instance"
4. Configure:
   - **Name**: video-downloader
   - **Compartment**: (your compartment)
   - **Availability Domain**: Any
   - **Shape**: VM.Standard.A1.Flex (Always Free)
   - **OCPU count**: 2 (free tier limit)
   - **Memory**: 6GB or 12GB (free tier limit)
   - **Operating System**: Oracle Linux or Ubuntu
5. Click "Next" until "Networking"
6. Configure:
   - **Assign a public IP address**: Yes
   - **Create virtual cloud network**: Create new VCN
7. Add SSH public key (generate with `ssh-keygen`)
8. Click "Create"

#### Step 3: Create Block Storage
1. Go to "Block Storage" → "Block Volumes"
2. Click "Create Block Volume"
3. Configure:
   - **Name**: downloads-storage
   - **Compartment**: (your compartment)
   - **Availability Domain**: Same as compute instance
   - **Size**: 200GB (free tier limit)
4. Click "Create"

#### Step 4: Attach Storage to Instance
1. Go to your compute instance
2. Click "Attached Block Volumes"
3. Click "Attach Block Volume"
4. Select the volume you created
5. Click "Attach"

#### Step 5: SSH into Instance
```bash
ssh -i ~/.ssh/your_key opc@YOUR_PUBLIC_IP
```

#### Step 6: Setup Docker
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Enable Docker
sudo systemctl enable docker
sudo systemctl start docker
```

#### Step 7: Mount Block Storage
```bash
# Format the volume (replace xvdb with actual device)
sudo mkfs.ext4 /dev/xvdb

# Create mount point
sudo mkdir -p /mnt/downloads

# Mount volume
sudo mount /dev/xvdb /mnt/downloads

# Add to fstab for auto-mount
echo '/dev/xvdb /mnt/downloads ext4 defaults 0 0' | sudo tee -a /etc/fstab

# Set permissions
sudo chown -R $USER:$USER /mnt/downloads
```

#### Step 8: Clone and Deploy
```bash
# Clone repo
git clone https://github.com/YOUR_USERNAME/video-downloader.git
cd video-downloader

# Modify docker-compose.yml to use mounted storage
# Update volumes: - /mnt/downloads:/app/downloads

# Build and run
docker-compose up -d
```

#### Step 9: Configure Firewall
```bash
# Open port 5000
sudo iptables -I INPUT -p tcp --dport 5000 -j ACCEPT
sudo iptables-save | sudo tee /etc/iptables.rules

# Or use Oracle Cloud Console:
# Go to Virtual Cloud Network → Security List → Add Ingress Rule
# Source: 0.0.0.0/0, Destination Port: 5000
```

#### Step 10: Access Your App
- Access at: `http://YOUR_PUBLIC_IP:5000`
- Set up domain with DNS (optional)
- Configure SSL with Let's Encrypt (optional)

---

### Option 1: Render.com (Step-by-Step)

#### Prerequisites
- GitHub account
- Render account (free)
- App code pushed to GitHub

#### Step 1: Prepare Your Repository
```bash
# Ensure your code is on GitHub
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/video-downloader.git
git push -u origin main
```

#### Step 2: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Verify email

#### Step 3: Deploy to Render
1. Click "New +" in dashboard
2. Select "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: video-downloader
   - **Branch**: main
   - **Runtime**: Docker
   - **Build Command**: (leave empty for Docker)
   - **Start Command**: (leave empty for Docker)
5. Click "Advanced"
6. Add Environment Variable:
   - Key: `PORT`
   - Value: `5000`
7. Click "Create Web Service"

#### Step 4: Add Persistent Disk
1. After deployment, go to your service
2. Click "Disks" tab
3. Click "New Disk"
4. Configure:
   - **Name**: downloads
   - **Mount Path**: /app/downloads
   - **Size**: 1GB (free tier limit)
5. Click "Create"

#### Step 5: Update Dockerfile for Render
The current Dockerfile needs a small adjustment for Render's disk mounting:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for yt-dlp
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates/ templates/

# Create downloads directory (will be mounted as persistent disk)
RUN mkdir -p downloads

EXPOSE 5000

CMD ["python", "app.py"]
```

#### Step 6: Access Your App
- Render will provide a URL like: `https://video-downloader.onrender.com`
- Automatic SSL is included
- App will be live after ~2-3 minutes

#### Step 7: Monitor and Troubleshoot
- View logs in Render dashboard
- Check "Metrics" for resource usage
- Free tier spins down after 15min inactivity

---

### Option 2: Railway.app (Step-by-Step)

#### Prerequisites
- GitHub account
- Railway account (free)
- App code pushed to GitHub

#### Step 1: Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Verify email

#### Step 2: Deploy to Railway
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your repository
4. Railway will auto-detect Docker
5. Click "Deploy"

#### Step 3: Configure Variables
1. Go to "Variables" tab
2. Add:
   - `PORT`: `5000`

#### Step 4: Add Persistent Volume
1. Go to "Volumes" tab
2. Click "New Volume"
3. Configure:
   - **Name**: downloads
   - **Mount Path**: /app/downloads
4. Click "Create"

#### Step 5: Access Your App
- Railway provides a URL like: `https://your-app.railway.app`
- Automatic SSL included

---

## Important Considerations

### Storage Limitations
- **Render**: 1GB free persistent storage
- **Railway**: 1GB free storage
- Downloads will fill storage quickly
- Consider auto-cleanup or user-managed deletion

### Performance Limitations
- **Render**: 512MB RAM, shared CPU
- **Railway**: 512MB RAM, shared CPU
- Large video downloads may be slow
- Concurrent downloads limited

---

## Solving Large File Download Issues on Render

Render's free tier has 3 main limitations for large downloads:

### 1. Memory Limit (512MB RAM)
**Problem**: Large videos can cause Out of Memory (OOM) errors during download or processing.

**Solutions:**

#### A. Stream Downloads Directly to Disk (Recommended)
Modify yt-dlp to write chunks directly to disk instead of buffering in memory. Your current implementation already does this with the `http_chunk_size` parameter (10MB chunks), which is good.

#### B. Limit Concurrent Downloads
Your app already limits to 5 concurrent downloads. For Render, reduce this to 1-2:

```python
# In app.py, change line 17:
executor = ThreadPoolExecutor(max_workers=2)  # Reduced from 5
```

#### C. Add File Size Limits
Reject videos larger than available storage:

```python
# Add to fetch_info endpoint
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB limit
if info.get('filesize') and info['filesize'] > MAX_FILE_SIZE:
    return jsonify({'error': f'File too large (max 100MB)'}), 400
```

---

### 2. Storage Limit (1GB)
**Problem**: Downloads will fill the 1GB disk quickly.

**Solutions:**

#### A. Automatic Cleanup After Download
Add auto-deletion after user downloads the file:

```python
# Modify /download/<task_id> endpoint
@app.route('/download/<task_id>')
def download_file(task_id):
    # ... existing code ...
    response = send_from_directory(DOWNLOAD_DIR, filename, as_attachment=True)

    # Schedule deletion after download
    @response.call_on_close
    def delete_after_download():
        try:
            os.remove(filepath)
            with tasks_lock:
                if task_id in tasks:
                    del tasks[task_id]
                    save_tasks()
        except:
            pass

    return response
```

#### B. Time-Based Auto-Cleanup
Delete files older than 1 hour:

```python
# Add to app.py
import threading
import time

def cleanup_old_files():
    while True:
        time.sleep(3600)  # Run every hour
        try:
            now = time.time()
            with tasks_lock:
                to_remove = []
                for task_id, task in tasks.items():
                    if task.get('completed') and (now - task['completed']) > 3600:
                        to_remove.append(task_id)
                        # Delete file
                        if task.get('filename'):
                            filepath = os.path.join(DOWNLOAD_DIR, task['filename'])
                            if os.path.exists(filepath):
                                os.remove(filepath)
                for task_id in to_remove:
                    del tasks[task_id]
                save_tasks()
        except Exception as e:
            print(f"Cleanup error: {e}")

# Start cleanup thread
cleanup_thread = threading.Thread(target=cleanup_old_files, daemon=True)
cleanup_thread.start()
```

#### C. Storage Quota Check
Reject downloads if storage is nearly full:

```python
def get_disk_usage():
    total, used, free = os.statvfs(DOWNLOAD_DIR)
    return (used / total) * 100

# In submit endpoint
disk_usage = get_disk_usage()
if disk_usage > 90:
    return jsonify({'error': 'Storage nearly full. Please clear downloads.'}), 507
```

---

### 3. Spin-Down Issue (15min inactivity)
**Problem**: Render spins down the app after 15 minutes, interrupting long downloads.

**Solutions:**

#### A. Use Keep-Alive Service
Set up a free cron job to ping your app every 10 minutes:

- **cron-job.org**: Free cron service
- **healthchecks.io**: Free monitoring with pings
- **UptimeRobot**: Free uptime monitoring

Configure to ping: `https://your-app.onrender.com/` every 10 minutes

#### B. Warn Users About Timeouts
Add a warning in the UI:

```html
<!-- Add to templates/index.html -->
<div class="warning">
  ⚠️ Free tier: Downloads over 15 minutes may be interrupted. 
  For large videos, consider downloading in smaller segments.
</div>
```

#### C. Implement Resume Capability
Use yt-dlp's resume feature (already supported by default with `--continue`):

```python
ydl_opts = {
    'outtmpl': os.path.join(out_dir, '%(title)s [%(id)s].%(ext)s'),
    'quiet': False,
    'no_warnings': False,
    'socket_timeout': 30,
    'http_chunk_size': 10485760,
    'progress_hooks': [lambda d: _progress_hook(d, task_id)] if task_id else [],
    'continue': True,  # Resume interrupted downloads
}
```

---

### 4. Network Timeout Issues
**Problem**: Slow downloads may timeout.

**Solutions:**

#### A. Increase Timeouts
```python
# In download_worker function
ydl_opts = {
    # ... existing options ...
    'socket_timeout': 60,  # Increased from 30
    'retries': 10,  # Add retry logic
    'fragment_retries': 10,
}
```

#### B. Use External Storage (Advanced)
Stream downloads directly to cloud storage instead of local disk:

- **Cloudflare R2**: Free 10GB storage + 10M egress requests/month
- **Backblaze B2**: 10GB free storage
- **Google Cloud Storage**: 5GB free storage

This requires significant code changes but solves storage limits completely.

---

### Recommended Configuration for Render

Combine these changes for best results:

1. **Reduce concurrent downloads** to 2
2. **Add 100MB file size limit**
3. **Implement time-based cleanup** (1 hour)
4. **Set up keep-alive ping** (cron-job.org)
5. **Add resume capability** (already in yt-dlp)
6. **Show storage usage** in UI

This configuration allows:
- Small to medium videos (under 100MB)
- Multiple users with auto-cleanup
- Reliable operation within Render's limits

### Ephemeral Storage Warning
- Free tiers may delete data if app is deleted
- Back up important downloads
- Implement cleanup in app (already have `/clear_all` endpoint)

### Network Restrictions
- Some platforms may block certain video sites
- yt-dlp may need updates for site changes
- Test with your target video sites

---

## Alternative: Self-Hosted (Free)

If you have a home computer or VPS, you can self-host:

### Requirements
- Always-on computer (Raspberry Pi, old PC, or VPS)
- Port forwarding or domain
- Docker installed

### Steps
```bash
# Clone repo
git clone https://github.com/YOUR_USERNAME/video-downloader.git
cd video-downloader

# Run with Docker
docker-compose up -d

# Access at http://localhost:5000
```

### Free VPS Options
- **Oracle Cloud Free Tier**: 2 ARM instances, 200GB storage
- **Google Cloud Free Tier**: e2-micro instance (limited)
- **AWS Free Tier**: 12 months EC2 t2.micro

---

## Recommended Choice

**For 5GB+ storage without ANY payment details**: Self-Hosting
- Unlimited storage (add external drives)
- No credit card or payment details required
- Complete control
- Free forever (if you have hardware)
- **ONLY option for your requirements**

**For 5GB+ storage with payment details**: Oracle Cloud Free Tier
- 200GB free storage (far exceeds 5GB)
- True always-on (no spin-down)
- Full control and performance
- Credit card for verification only (no charges)

**For 5GB+ storage with Cloudflare payment details**: Cloudflare R2 + Render
- 10GB free storage (meets 5GB requirement)
- No egress fees (unique to Cloudflare)
- Requires payment details for Cloudflare account
- App code already configured for R2

**For quick testing (under 1GB)**: Render.com
- Simplest setup
- No payment details required
- But only 1GB storage (not enough for your needs)

---

## Post-Deployment Checklist

- [ ] Test video download functionality
- [ ] Verify persistent storage works
- [ ] Check SSL certificate
- [ ] Monitor resource usage
- [ ] Test cleanup endpoints
- [ ] Set up monitoring alerts
- [ ] Document backup strategy
- [ ] Test with various video sites

---

## Troubleshooting

### Render: App won't start
- Check build logs in Render dashboard
- Verify Dockerfile syntax
- Ensure PORT environment variable is set

### Railway: Deployment fails
- Check Railway logs
- Verify Docker build succeeds locally
- Check GitHub webhook settings

### Storage issues
- Monitor disk usage in platform dashboard
- Implement automatic cleanup
- Use `/clear_all` endpoint regularly

### Download failures
- Check yt-dlp is latest version
- Verify FFmpeg is installed
- Check network connectivity
- Review error logs

---

## Cost Estimate (Beyond Free Tier)

If you exceed free limits:

**Render:**
- $7/month for 512MB RAM + 1GB storage
- $5/month per additional 1GB storage

**Railway:**
- $5/month base (after free credit)
- $0.25/GB storage

**Oracle Cloud:**
- Always free (within limits)
