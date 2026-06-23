# Render Deployment Guide (1GB Free Tier)

Deploy your video downloader to Render.com with 1GB free storage.

**Note:** This uses Render's free tier with 1GB storage. Files auto-delete after 1 hour to manage the limited space.

---

## Prerequisites

- Render account (free, no credit card required)
- GitHub account
- Your video downloader code

---

## Step 1: Create Render Account

1. Go to [render.com](https://render.com)
2. Click "Sign Up"
3. Sign up with GitHub
4. Verify email
5. No credit card required

---

## Step 2: Push Code to GitHub

```bash
# If not already on GitHub
git init
git add .
git commit -m "Ready for Render deployment"
git branch -M main

# Add your GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/video-downloader.git

# Push to GitHub
git push -u origin main
```

---

## Step 3: Create Web Service on Render

1. In Render dashboard, click **New +**
2. Select **Web Service**
3. Click **Connect GitHub**
4. Authorize Render to access your GitHub
5. Select your `video-downloader` repository
6. Select the `main` branch

---

## Step 4: Configure Web Service

1. **Name**: `video-downloader`
2. **Branch**: `main`
3. **Runtime**: Docker (Render should auto-detect from Dockerfile)
4. **Build Command**: Leave empty (Docker handles this)
5. **Start Command**: Leave empty (Docker handles this)

---

## Step 5: Add Environment Variables

Scroll down to **Advanced** → **Environment Variables**. Add:

| Key | Value |
|-----|-------|
| `PORT` | `5000` |

---

## Step 6: Deploy

1. Click **Create Web Service**
2. Render will build your Docker image
3. Wait for deployment to complete (2-5 minutes)
4. Check the logs for successful startup

---

## Step 7: Get Your App URL

After deployment, Render will provide a URL like:
- `https://video-downloader.onrender.com`

---

## Step 8: Test Deployment

1. Open your app URL in browser
2. Paste a YouTube/video URL
3. Click "Fetch Info"
4. Verify video info loads
5. Click "Download"
6. Wait for download to complete
7. Test download endpoint

---

## Storage Management

### Automatic Cleanup
- Files auto-delete after 1 hour
- This manages the 1GB storage limit
- Check logs for cleanup messages

### Manual Cleanup
- Use the `/clear_all` endpoint in your app
- Clears all completed, error, and cancelled downloads
- Keeps running downloads intact

### Monitor Storage
- Go to Render Dashboard → your service
- Check disk usage in logs
- If storage is full, use `/clear_all`

---

## Render Free Tier Limits

**Resources:**
- 512MB RAM
- Shared CPU
- 1GB persistent storage
- 750 hours/month free

**Limitations:**
- Spins down after 15 minutes of inactivity
- Takes ~30 seconds to wake up
- Only 1GB storage (not enough for large video collections)

**Best for:**
- Personal use
- Testing
- Small-scale downloads
- Occasional use

---

## Keep-Alive (Optional)

Render spins down after 15 minutes of inactivity. To prevent this:

1. Go to [cron-job.org](https://cron-job.org)
2. Create free account
3. Create cron job:
   - URL: `https://your-app.onrender.com/`
   - Minutes: Every 10 minutes
4. This keeps your app awake

---

## Troubleshooting

### Issue: Deployment fails
**Solution:**
- Check Render build logs
- Verify Dockerfile is valid
- Ensure requirements.txt is correct

### Issue: App spins down frequently
**Solution:**
- Set up keep-alive cron job
- Or accept the spin-down (normal for free tier)

### Issue: Storage full
**Solution:**
- Use `/clear_all` endpoint
- Files auto-delete after 1 hour
- Monitor usage in logs

### Issue: Download timeout
**Solution:**
- Render may spin down during long downloads
- Set up keep-alive
- Or accept that very long downloads may fail

---

## Automated Deployment

Render has built-in auto-deploy from GitHub:

```bash
# Make changes
git add .
git commit -m "Update app"
git push origin main

# Render automatically:
# 1. Detects the push
# 2. Builds new Docker image
# 3. Deploys to production
# 4. Updates your app
```

No additional setup needed - auto-deploy is enabled by default when you connect GitHub.

---

## Environment Variables Reference

| Variable | Required | Description | Value |
|----------|----------|-------------|-------|
| `PORT` | Yes | Port for Flask app | `5000` |

---

## Cost Summary

**Free Tier:**
- 512MB RAM
- Shared CPU
- 1GB storage
- **Total cost: $0/month**

**If you exceed limits:**
- Paid tier: $7/month
- More RAM, CPU, and storage

---

## Security Best Practices

1. **Never commit credentials to Git**
   - No secrets in code
   - Use environment variables only

2. **Monitor your app**
   - Check Render logs regularly
   - Watch for unusual activity

3. **Keep dependencies updated**
   - Update requirements.txt regularly
   - Re-deploy after updates

---

## Next Steps

1. ✅ Create Render account
2. ✅ Push code to GitHub
3. ✅ Create web service on Render
4. ✅ Configure environment variables
5. ✅ Deploy and test
6. ✅ Set up keep-alive (optional)
7. ✅ Share your app URL

---

## Support

- Render Docs: https://render.com/docs
- Your app logs: Render Dashboard → Logs
- Render Dashboard: https://dashboard.render.com
