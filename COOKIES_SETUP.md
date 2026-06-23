# YouTube Cookies Setup Guide

How to export cookies from your browser to bypass YouTube bot detection in yt-dlp.

---

## Why You Need Cookies

YouTube sometimes blocks automated downloads with bot detection. Using your browser's cookies makes yt-dlp appear as a legitimate user, allowing downloads to work.

---

## Method 1: Browser Extension (Recommended)

### For Chrome/Edge/Brave

1. **Install Extension**
   - Go to Chrome Web Store
   - Search: "Get cookies.txt LOCALLY"
   - Install the extension by Kairi
   - Alternative: "cookies.txt" extension

2. **Export Cookies**
   - Open YouTube and sign in to your account
   - Click the extension icon in your browser toolbar
   - Click "Export" or "Download"
   - Save as `cookies.txt`

3. **Upload to Render**
   - Place `cookies.txt` in your project root
   - Commit to Git (or add as environment variable)
   - Set `COOKIE_FILE=/app/cookies.txt` in Render environment variables

### For Firefox

1. **Install Extension**
   - Go to Firefox Add-ons
   - Search: "cookies.txt"
   - Install the extension

2. **Export Cookies**
   - Open YouTube and sign in
   - Click the extension icon
   - Export cookies as `cookies.txt`

---

## Method 2: yt-dlp Built-in Export

### Using Command Line

```bash
# Export cookies from Chrome (Windows)
yt-dlp --cookies-from-browser chrome URL

# Export cookies from Chrome (Mac)
yt-dlp --cookies-from-browser chrome URL

# Export cookies from Firefox
yt-dlp --cookies-from-browser firefox URL

# Export cookies from Edge
yt-dlp --cookies-from-browser edge URL
```

### Save to File

```bash
# Export and save to file
yt-dlp --cookies-from-browser chrome --cookies cookies.txt URL
```

---

## Method 3: Manual Export (Advanced)

### Chrome

1. Open YouTube and sign in
2. Press F12 to open Developer Tools
3. Go to **Application** tab
4. Expand **Cookies** → Select `https://www.youtube.com`
5. Copy all cookies to a text file in Netscape format

### Firefox

1. Open YouTube and sign in
2. Press F12 to open Developer Tools
3. Go to **Storage** tab
4. Expand **Cookies** → Select `https://www.youtube.com`
5. Export cookies using a browser extension

---

## Cookie File Format

The `cookies.txt` file should be in Netscape format:

```
# Netscape HTTP Cookie File
.youtube.com	TRUE	/	FALSE	1735689600	SID	xxxxx
.youtube.com	TRUE	/	FALSE	1735689600	HSID	xxxxx
.youtube.com	TRUE	/	FALSE	1735689600	SSID	xxxxx
```

---

## Deploying with Render

### Option 1: Commit cookies.txt (Not Recommended)

```bash
# Add cookies.txt to project
cp cookies.txt /path/to/video-downloader/
git add cookies.txt
git commit -m "Add cookies.txt"
git push origin main
```

**Warning:** This commits your personal cookies to Git. Not secure for public repositories.

### Option 2: Environment Variable (Recommended)

1. **Encode cookies.txt as base64**
   ```bash
   # On Linux/Mac
   base64 -w 0 cookies.txt > cookies.b64
   
   # On Windows (PowerShell)
   [Convert]::ToBase64String([IO.File]::ReadAllBytes("cookies.txt")) > cookies.b64
   ```

2. **Add to Render Environment Variables**
   - Key: `COOKIES_BASE64`
   - Value: (paste the base64 string)

3. **Update app.py to decode**
   ```python
   import base64
   
   COOKIES_BASE64 = os.environ.get('COOKIES_BASE64')
   if COOKIES_BASE64:
       with open(COOKIE_FILE, 'wb') as f:
           f.write(base64.b64decode(COOKIES_BASE64))
   ```

### Option 3: Render Disk (Best for Render)

1. **Upload cookies.txt via Render Dashboard**
   - Go to your service → Disk
   - Upload `cookies.txt` to `/app/cookies.txt`

2. **Set environment variable**
   - Key: `COOKIE_FILE`
   - Value: `/app/cookies.txt`

---

## Security Notes

**Important Security Considerations:**

1. **Cookies contain your login credentials**
   - Anyone with your cookies can access your YouTube account
   - Never share cookies.txt publicly
   - Don't commit to public Git repositories

2. **Cookies expire**
   - YouTube cookies expire periodically
   - You'll need to re-export them occasionally
   - Update your deployment when cookies expire

3. **Use a separate YouTube account**
   - Create a dedicated YouTube account for downloads
   - Don't use your main personal account
   - Reduces security risk

---

## Testing Cookies

### Test Locally

```bash
# Test with cookies
yt-dlp --cookies cookies.txt "https://www.youtube.com/watch?v=VIDEO_ID"

# Test without cookies (for comparison)
yt-dlp "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Test in App

1. Add `cookies.txt` to your project
2. Run the app locally
3. Try downloading a YouTube video
4. Check logs for "Using cookies from: /app/cookies.txt"

---

## Troubleshooting

### Issue: "Cookie file not found"
**Solution:** 
- Verify cookies.txt is in the correct location
- Check COOKIE_FILE environment variable
- Ensure file permissions allow reading

### Issue: "Cookies expired"
**Solution:**
- Re-export cookies from browser
- Update cookies.txt in deployment
- Redeploy the app

### Issue: Still getting bot detection
**Solution:**
- Ensure you're signed into YouTube when exporting
- Try a different browser for cookie export
- Update yt-dlp to latest version
- Check that cookies.txt is in correct format

### Issue: Downloads work locally but not on Render
**Solution:**
- Verify cookies.txt is deployed to Render
- Check COOKIE_FILE environment variable on Render
- View Render logs for cookie-related errors

---

## Alternative: No Cookies

If you don't want to use cookies, try these alternatives:

1. **Update yt-dlp regularly**
   - YouTube changes detection frequently
   - New yt-dlp versions often bypass detection

2. **Use different video sources**
   - Try Vimeo, Dailymotion, or other platforms
   - Some YouTube videos are less protected

3. **Accept limitations**
   - Some videos may not download without cookies
   - This is YouTube's anti-bot measure

---

## Summary

**Recommended Setup:**
1. Install "Get cookies.txt LOCALLY" browser extension
2. Export cookies from YouTube while signed in
3. Save as `cookies.txt`
4. Deploy securely (base64 encoding or Render disk)
5. Set `COOKIE_FILE=/app/cookies.txt` environment variable
6. Test downloads

**Security Best Practices:**
- Don't commit cookies to public Git
- Use a dedicated YouTube account
- Re-export cookies when they expire
- Keep cookies.txt private
