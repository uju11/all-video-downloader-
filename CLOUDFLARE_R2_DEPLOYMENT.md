# Cloudflare R2 + Render Deployment Guide

Complete guide to deploy your video downloader using Cloudflare R2 (10GB free storage) and Render (free hosting).

---

## Prerequisites

- Cloudflare account (free, no credit card required)
- Render account (free, no credit card required)
- GitHub account
- Your video downloader code

---

## Part 1: Cloudflare R2 Setup

### Step 1: Create Cloudflare Account
1. Go to [cloudflare.com](https://cloudflare.com)
2. Click "Sign Up"
3. Use email or Google/GitHub account
4. No credit card required

### Step 2: Create R2 Bucket
1. After signup, go to Cloudflare Dashboard
2. In the left sidebar, click **R2** (under Storage)
3. Click **Create bucket**
4. Configure:
   - **Bucket name**: `video-downloads` (or your preferred name)
   - **Location**: Choose nearest region (e.g., "APAC" if in Asia)
5. Click **Create bucket**

### Step 3: Get Your Account ID
1. In Cloudflare Dashboard, click your profile (top right)
2. Select **My Profile**
3. Copy the **Account ID** (you'll need this for the endpoint)
4. Your R2 endpoint will be: `https://YOUR_ACCOUNT_ID.r2.cloudflarestorage.com`

### Step 4: Create R2 API Token
1. Go to **R2** → **Manage R2 API Tokens**
2. Click **Create API Token**
3. Configure:
   - **Token name**: `video-downloader`
   - **Permissions**: 
     - Object Read & Write
   - **TTL**: Leave as "Forever" or set a long expiry
   - **Account resources**: Select your account
   - **Bucket permissions**: 
     - Include: `video-downloads` (your bucket name)
     - Access: Read & Write
4. Click **Create API Token**
5. **IMPORTANT**: Copy and save these credentials (you won't see them again):
   - Access Key ID
   - Secret Access Key

### Step 5: Verify R2 Setup
1. Go to R2 → your bucket
2. You should see an empty bucket
3. Try uploading a test file via the dashboard to verify it works

---

## Part 2: Prepare Your Code

### Step 1: Update Environment Variables
Your app already has R2 support. You just need to set the environment variables.

### Step 2: Push Code to GitHub
```bash
# If not already on GitHub
git init
git add .
git commit -m "Add R2 support"
git branch -M main

# Add your GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/video-downloader.git

# Push to GitHub
git push -u origin main
```

---

## Part 3: Deploy to Render

### Step 1: Create Render Account
1. Go to [render.com](https://render.com)
2. Click "Sign Up"
3. Sign up with GitHub
4. Verify email
5. No credit card required

### Step 2: Create New Web Service
1. In Render dashboard, click **New +**
2. Select **Web Service**
3. Click **Connect GitHub**
4. Authorize Render to access your GitHub
5. Select your `video-downloader` repository
6. Select the `main` branch

### Step 3: Configure Web Service
1. **Name**: `video-downloader`
2. **Branch**: `main`
3. **Runtime**: Docker (Render should auto-detect from Dockerfile)
4. **Build Command**: Leave empty (Docker handles this)
5. **Start Command**: Leave empty (Docker handles this)

### Step 4: Add Environment Variables
Scroll down to **Advanced** → **Environment Variables**. Add these:

| Key | Value |
|-----|-------|
| `USE_R2` | `true` |
| `R2_BUCKET` | `video-downloads` (your bucket name) |
| `R2_ENDPOINT` | `https://YOUR_ACCOUNT_ID.r2.cloudflarestorage.com` |
| `R2_ACCESS_KEY` | Your Access Key ID from Step 1.4 |
| `R2_SECRET_KEY` | Your Secret Access Key from Step 1.4 |
| `PORT` | `5000` |

### Step 5: Deploy
1. Click **Create Web Service**
2. Render will build your Docker image
3. Wait for deployment to complete (2-5 minutes)
4. Check the logs for "R2 storage enabled" message

### Step 6: Get Your App URL
After deployment, Render will provide a URL like:
- `https://video-downloader.onrender.com`

---

## Part 4: Verify Deployment

### Step 1: Check Render Logs
1. Go to your web service in Render
2. Click **Logs**
3. Look for: "R2 storage enabled"
4. If you see errors, check the environment variables

### Step 2: Test Video Download
1. Open your app URL in browser
2. Paste a YouTube/video URL
3. Click "Fetch Info"
4. Verify video info loads
5. Click "Download"
6. Wait for download to complete

### Step 3: Verify R2 Upload
1. Go to Cloudflare Dashboard → R2 → your bucket
2. You should see the downloaded video file
3. Verify the file size matches the video

### Step 4: Test Download Endpoint
1. Click the download button for your completed task
2. Browser should redirect to R2 and download the file
3. Verify the file plays correctly

---

## Part 5: Monitor and Maintain

### Monitor R2 Usage
1. Go to Cloudflare Dashboard → R2
2. Check storage usage (10GB free limit)
3. Check egress requests (10M free per month)

### Monitor Render Usage
1. Go to Render dashboard → your service
2. Check CPU/Memory usage
3. Check bandwidth usage

### Set Up Keep-Alive (Optional)
Render spins down after 15 minutes of inactivity. To prevent this:

1. Go to [cron-job.org](https://cron-job.org)
2. Create free account
3. Create cron job:
   - URL: `https://your-app.onrender.com/`
   - Minutes: Every 10 minutes
4. This keeps your app awake

---

## Troubleshooting

### Issue: "R2 storage disabled" in logs
**Cause**: Missing or incorrect environment variables
**Solution**: 
- Verify all 5 R2 environment variables are set in Render
- Check for typos in keys/values
- Ensure R2_ENDPOINT includes your Account ID

### Issue: "R2 upload failed"
**Cause**: Incorrect credentials or permissions
**Solution**:
- Regenerate API tokens in Cloudflare
- Verify bucket permissions include Read & Write
- Check bucket name matches R2_BUCKET variable

### Issue: Downloads fail with timeout
**Cause**: Render spin-down or network issues
**Solution**:
- Set up keep-alive cron job
- Increase socket timeout in app.py (currently 60s)
- Check Render logs for specific error

### Issue: Presigned URL expires too quickly
**Cause**: 1-hour expiry may be too short
**Solution**:
- Edit app.py line 393: change `ExpiresIn=3600` to `ExpiresIn=86400` (24 hours)

### Issue: Storage nearly full
**Cause**: Approaching 10GB R2 limit
**Solution**:
- Use `/clear_all` endpoint in your app
- Manually delete old files from R2 dashboard
- Files auto-delete after 24 hours (configured in app)

### Issue: Build fails on Render
**Cause**: Dockerfile or dependency issues
**Solution**:
- Check Render build logs
- Verify requirements.txt includes boto3
- Ensure Dockerfile is valid

---

## Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `USE_R2` | Yes | Enable R2 storage | `true` |
| `R2_BUCKET` | Yes | Your R2 bucket name | `video-downloads` |
| `R2_ENDPOINT` | Yes | Your R2 API endpoint | `https://abc123.r2.cloudflarestorage.com` |
| `R2_ACCESS_KEY` | Yes | Your R2 access key ID | `abc123def456` |
| `R2_SECRET_KEY` | Yes | Your R2 secret key | `xyz789uvw012` |
| `PORT` | Yes | Port for Flask app | `5000` |

---

## Cost Summary

**Free Tier Limits:**
- Cloudflare R2: 10GB storage, 10M egress requests/month
- Render: 512MB RAM, shared CPU, 1GB disk (not used with R2)
- **Total cost: $0/month**

**If you exceed limits:**
- R2: $0.015/GB storage beyond 10GB
- R2: No egress fees (unique to Cloudflare)
- Render: $7/month for paid tier

---

## Security Best Practices

1. **Never commit credentials to Git**
   - Use environment variables only
   - Don't add .env files to repository

2. **Rotate API keys regularly**
   - Regenerate R2 tokens every 90 days
   - Update Render environment variables

3. **Use presigned URLs**
   - App already uses presigned URLs (1-hour expiry)
   - Consider extending to 24 hours if needed

4. **Monitor for unusual activity**
   - Check R2 usage regularly
   - Review Render logs for errors

---

## Next Steps

1. ✅ Complete Cloudflare R2 setup
2. ✅ Deploy to Render with environment variables
3. ✅ Test download and upload functionality
4. ✅ Set up monitoring and alerts
5. ✅ Configure keep-alive if needed
6. ✅ Share your app URL with users

---

## Support

- Cloudflare R2 Docs: https://developers.cloudflare.com/r2/
- Render Docs: https://render.com/docs
- Your app logs: Render Dashboard → Logs
- R2 Dashboard: Cloudflare Dashboard → R2
