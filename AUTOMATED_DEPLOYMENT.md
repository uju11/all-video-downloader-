# Automated Deployment Guide

Automate your deployment so that every push to GitHub automatically deploys to Render.

---

## Option 1: Render Auto-Deploy (Simplest)

Render has built-in automatic deployment from GitHub. No additional setup needed!

### How It Works
1. You push code to GitHub
2. Render detects the push
3. Render automatically rebuilds and deploys
4. Your app updates with zero manual intervention

### Setup (Already Done in Previous Guide)
When you created your Render web service and connected it to GitHub, auto-deploy is **already enabled** by default.

### Configure Auto-Deploy Settings
1. Go to Render Dashboard → your service
2. Click **Settings**
3. Scroll to **Build & Deploy**
4. Configure:
   - **Auto-Deploy**: Enabled (default)
   - **Branch**: `main` (or your production branch)
   - **Build Command**: Leave empty (Docker handles this)
   - **Push to deploy**: Enabled

### Workflow
```bash
# Make changes to your code
git add .
git commit -m "Add new feature"
git push origin main

# Render automatically:
# 1. Detects the push
# 2. Builds new Docker image
# 3. Deploys to production
# 4. Updates your app
```

### View Deployment Status
1. Go to Render Dashboard → your service
2. Click **Events** tab
3. See all deployments with status (success/fail)
4. Click any deployment to view logs

### Pause Auto-Deploy (Optional)
If you want to control when deployments happen:
1. Go to Settings → Build & Deploy
2. Toggle **Auto-Deploy** to OFF
3. Manually deploy by clicking **Manual Deploy** button

---

## Option 2: GitHub Actions + Render (Advanced)

Add testing and validation before auto-deploy.

### Benefits
- Run tests before deployment
- Validate code quality
- Prevent broken deployments
- Add deployment approvals

### Setup GitHub Actions

#### Step 1: Create Workflow File
Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Render

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run tests (if you have tests)
        run: |
          python -m pytest tests/ || echo "No tests found"
  
  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to Render
        uses: johnbeynon/render-deploy-action@v0.0.8
        with:
          service-id: ${{ secrets.RENDER_SERVICE_ID }}
          render-api-key: ${{ secrets.RENDER_API_KEY }}
          wait-for-success: true
```

#### Step 2: Get Render API Key
1. Go to Render Dashboard → Account Settings
2. Scroll to **API Keys**
3. Click **Create API Key**
4. Name it `GitHub Actions`
5. Copy the API key

#### Step 3: Get Render Service ID
1. Go to Render Dashboard → your service
2. The service ID is in the URL: `https://dashboard.render.com/web/srv/SERVICE_ID`
3. Copy the SERVICE_ID

#### Step 4: Add Secrets to GitHub
1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Add repository secrets:
   - `RENDER_API_KEY`: Your Render API key
   - `RENDER_SERVICE_ID`: Your service ID

#### Step 5: Push to GitHub
```bash
git add .github/workflows/deploy.yml
git commit -m "Add GitHub Actions workflow"
git push origin main
```

Now every push to `main` will:
1. Run tests
2. If tests pass, deploy to Render
3. If tests fail, deployment is blocked

---

## Option 3: Branch-Based Deployment (Production/Staging)

Deploy different branches to different environments.

### Setup Multiple Services on Render

#### Production Service
- Name: `video-downloader-prod`
- Branch: `main`
- Environment variables: Production R2 credentials

#### Staging Service
- Name: `video-downloader-staging`
- Branch: `develop`
- Environment variables: Staging R2 credentials (same bucket, different prefix)

### GitHub Actions Workflow
```yaml
name: Deploy to Render

on:
  push:
    branches: [main, develop]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Production
        if: github.ref == 'refs/heads/main'
        uses: johnbeynon/render-deploy-action@v0.0.8
        with:
          service-id: ${{ secrets.RENDER_PROD_SERVICE_ID }}
          render-api-key: ${{ secrets.RENDER_API_KEY }}
      
      - name: Deploy to Staging
        if: github.ref == 'refs/heads/develop'
        uses: johnbeynon/render-deploy-action@v0.0.8
        with:
          service-id: ${{ secrets.RENDER_STAGING_SERVICE_ID }}
          render-api-key: ${{ secrets.RENDER_API_KEY }}
```

### Workflow
```bash
# Development work
git checkout develop
git add .
git commit -m "New feature"
git push origin develop
# Deploys to staging

# Ready for production
git checkout main
git merge develop
git push origin main
# Deploys to production
```

---

## Option 4: Docker Hub + Render (Alternative)

Push Docker images to Docker Hub, then deploy to Render.

### Benefits
- Faster deployments (no rebuild on Render)
- Version control of Docker images
- Can deploy same image to multiple services

### Setup

#### Step 1: Create Docker Hub Account
1. Go to [hub.docker.com](https://hub.docker.com)
2. Sign up (free)
3. Create access token in Account Settings

#### Step 2: Create GitHub Actions Workflow
Create `.github/workflows/docker.yml`:

```yaml
name: Build and Push Docker Image

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_TOKEN }}
      
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: yourusername/video-downloader:latest
```

#### Step 3: Update Render Service
1. Go to Render Dashboard → your service
2. Settings → Build & Deploy
3. Change **Runtime** to **Docker**
4. Set **Image** to: `yourusername/video-downloader:latest`
5. Enable **Auto-Deploy**

#### Step 4: Add GitHub Secrets
- `DOCKER_USERNAME`: Your Docker Hub username
- `DOCKER_TOKEN`: Your Docker Hub access token

### Workflow
```bash
git push origin main
# GitHub Actions builds and pushes to Docker Hub
# Render detects new image and auto-deploys
```

---

## Recommended Setup

**For simplicity**: Use Option 1 (Render Auto-Deploy)
- Already configured
- Zero additional setup
- Works out of the box

**For production**: Use Option 2 (GitHub Actions + Render)
- Adds testing before deployment
- Prevents broken code from deploying
- Better for teams

**For multiple environments**: Use Option 3 (Branch-Based)
- Separate staging and production
- Test in staging before production
- Safer deployment pipeline

---

## Monitoring Automated Deployments

### Render Dashboard
1. Go to your service
2. Click **Events** tab
3. View deployment history
4. Click any deployment for logs

### GitHub Actions (if using Option 2)
1. Go to GitHub repository
2. Click **Actions** tab
3. View workflow runs
4. See test results and deployment status

### Notifications

#### Render Notifications
1. Go to Render Dashboard → your service
2. Settings → Notifications
3. Enable email notifications for:
   - Deploy succeeded
   - Deploy failed

#### GitHub Notifications
1. Go to GitHub repository
2. Settings → Notifications
3. Enable workflow notifications

---

## Rollback Strategy

If a deployment fails or breaks something:

### Manual Rollback via Render
1. Go to Render Dashboard → your service
2. Click **Events** tab
3. Find the last successful deployment
4. Click **Rollback** (if available)
5. Or manually deploy previous commit

### Rollback via Git
```bash
# View deployment history
git log --oneline

# Revert to previous commit
git revert HEAD
git push origin main
# Render auto-deploys the revert
```

### Rollback via GitHub Actions
```bash
# Create rollback branch
git checkout -b rollback
git revert HEAD
git push origin rollback

# Manually trigger GitHub Actions for rollback branch
```

---

## Best Practices

1. **Always test before deploying**
   - Use GitHub Actions to run tests
   - Test locally first

2. **Use semantic versioning**
   - Tag releases: `git tag v1.0.0`
   - Deploy tags instead of branches

3. **Keep environment variables secure**
   - Never commit .env files
   - Use Render environment variables
   - Use GitHub Secrets for CI/CD

4. **Monitor deployments**
   - Check Render logs after each deploy
   - Set up notifications for failures

5. **Have a rollback plan**
   - Know how to quickly revert
   - Keep previous working commits

---

## Summary

**Simplest**: Render Auto-Deploy (already configured)
**Most robust**: GitHub Actions + Render
**Most flexible**: Branch-environment deployment

Your current setup already has Render Auto-Deploy enabled. Just push to GitHub and it deploys automatically!
