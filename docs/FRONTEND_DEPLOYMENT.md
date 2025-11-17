# Frontend Console Deployment Guide

This guide walks you through deploying the React admin console to Google App Engine.

## Overview

The frontend console is deployed as a static site on Google App Engine, which provides:
- ✅ Global CDN distribution
- ✅ Automatic SSL certificates
- ✅ Custom domain support
- ✅ Zero-downtime deployments
- ✅ Version management
- ✅ Easy rollbacks

## Prerequisites

1. **Google Cloud SDK** installed and configured
   ```bash
   gcloud --version
   ```

2. **Authenticated with gcloud**
   ```bash
   gcloud auth login
   ```

3. **Project configured**
   ```bash
   gcloud config set project YOUR-PROJECT-ID
   ```

4. **App Engine initialized**
   ```bash
   # Only needed once per project
   gcloud app create --region=us-central
   ```

5. **Production WorkOS credentials** ready

## Step-by-Step Deployment

### 1. Configure Production Environment

Create `.env.production.local` in `frontend/console/`:

```bash
cd frontend/console
cp .env.production .env.production.local
```

Edit `.env.production.local` with your values:

```bash
# Backend GraphQL API (your Cloud Run service URL)
VITE_GRAPHQL_URL=https://core-SERVICE_HASH-uc.a.run.app/graphql/

# WorkOS Production Credentials
VITE_WORKOS_CLIENT_ID=client_01XXXXXXXXXXXXX

# App Engine URL (replace YOUR-PROJECT-ID with actual project ID)
VITE_WORKOS_REDIRECT_URI=https://console-dot-YOUR-PROJECT-ID.uc.r.appspot.com/auth/callback
```

**Finding your backend URL**:
```bash
gcloud run services describe core --region=us-central1 --format='value(status.url)'
```

### 2. Configure WorkOS

Add the production redirect URI to your WorkOS dashboard:

1. Go to https://dashboard.workos.com
2. Select your environment/organization
3. Navigate to **Redirect URIs**
4. Add: `https://console-dot-YOUR-PROJECT-ID.uc.r.appspot.com/auth/callback`
5. Save changes

### 3. Review app.yaml

The `app.yaml` file is pre-configured for static site hosting. Review it:

```yaml
runtime: python312
service: console

handlers:
  - url: /
    static_files: dist/index.html
    # ... more handlers ...
```

**Key features**:
- Service name: `console` (creates console-dot-PROJECT-ID.uc.r.appspot.com)
- Assets cached for 1 year (with immutable flag)
- HTML files not cached (for instant updates)
- Favicon files configured
- Client-side routing support

### 4. Deploy

```bash
npm run deploy
```

This command will:
1. Build the app with production environment variables
2. Create optimized production bundle
3. Deploy to App Engine
4. Deploy as the `console` service

**Manual deployment**:
```bash
npm run build:prod
gcloud app deploy app.yaml --quiet
```

### 5. Verify Deployment

After deployment completes:

1. **Visit the URL**:
   ```
   https://console-dot-YOUR-PROJECT-ID.uc.r.appspot.com
   ```

2. **Test authentication**:
   - Click login
   - Should redirect to WorkOS
   - Authenticate with your credentials
   - Should redirect back and show dashboard

3. **Check browser console** for any errors

## App Engine Management

### View Deployed Versions

```bash
gcloud app versions list --service=console
```

### View Logs

```bash
# Real-time logs
gcloud app logs tail --service=console

# Recent logs
gcloud app logs read --service=console --limit=50
```

### Traffic Splitting (for gradual rollouts)

```bash
# Split traffic: 90% to current, 10% to new version
gcloud app services set-traffic console --splits=v1=0.9,v2=0.1
```

### Rollback to Previous Version

```bash
# List versions
gcloud app versions list --service=console

# Route all traffic to previous version
gcloud app services set-traffic console --splits=VERSION_ID=1.0
```

### Delete Old Versions

```bash
# Delete a specific version
gcloud app versions delete VERSION_ID --service=console
```

## Custom Domain Setup

### 1. Add Custom Domain

```bash
gcloud app domain-mappings create console.yourdomain.com \
  --certificate-management=automatic
```

### 2. Update DNS Records

Add the DNS records shown by the command above to your domain provider.

### 3. Update WorkOS Redirect URI

Add your custom domain redirect URI:
```
https://console.yourdomain.com/auth/callback
```

### 4. Update Environment Variable

Update `.env.production.local`:
```bash
VITE_WORKOS_REDIRECT_URI=https://console.yourdomain.com/auth/callback
```

Re-deploy:
```bash
npm run deploy
```

## Updating the Application

### Regular Updates

```bash
# 1. Pull latest code
git pull origin main

# 2. Install dependencies (if package.json changed)
npm install

# 3. Deploy
npm run deploy
```

### Environment Variable Changes

1. Update `.env.production.local`
2. Re-deploy: `npm run deploy`

### Rollback if Issues Occur

```bash
# List versions
gcloud app versions list --service=console

# Route traffic to previous version
gcloud app services set-traffic console --splits=PREVIOUS_VERSION=1.0
```

## Troubleshooting

### Build Fails

**Check Node version**:
```bash
node --version  # Should be 24.x
nvm use         # Uses .nvmrc
```

**Clear cache and rebuild**:
```bash
rm -rf node_modules dist
npm install
npm run build:prod
```

### Deployment Fails

**Check gcloud authentication**:
```bash
gcloud auth list
gcloud config get-value project
```

**Check App Engine quota**:
- Visit Google Cloud Console → App Engine → Quotas

**Check app.yaml syntax**:
```bash
gcloud app deploy app.yaml --validate-only
```

### Authentication Not Working

**Check WorkOS redirect URI**:
- Must match exactly: `https://console-dot-PROJECT-ID.uc.r.appspot.com/auth/callback`
- Check for trailing slashes
- Verify in WorkOS dashboard

**Check environment variables**:
```bash
# Verify build includes correct env vars
npm run build:prod
cat dist/assets/index-*.js | grep "WORKOS_CLIENT_ID"
```

**Check browser console**:
- Open DevTools → Console
- Look for CORS errors, network failures

### 404 Errors on Page Refresh

This indicates client-side routing isn't working. Check `app.yaml`:

```yaml
# Catch-all handler should be present
- url: /.*
  static_files: dist/index.html
  upload: dist/index.html
```

### Static Assets Not Loading

**Check cache headers**:
```bash
curl -I https://console-dot-PROJECT-ID.uc.r.appspot.com/assets/index.js
```

Should see:
```
Cache-Control: public, max-age=31536000, immutable
```

## Performance Optimization

### Enable Cloud CDN

Cloud CDN is automatically enabled for App Engine static files.

### Monitor Performance

1. **App Engine Dashboard**:
   - Cloud Console → App Engine → Dashboard
   - View latency, traffic, errors

2. **Lighthouse Audit**:
   ```bash
   npm install -g lighthouse
   lighthouse https://console-dot-PROJECT-ID.uc.r.appspot.com
   ```

### Optimize Build

The build is already optimized with:
- Code splitting
- Tree shaking
- Minification
- Asset hashing
- Gzip compression

## Cost Considerations

**App Engine Standard Pricing**:
- Free tier: 28 instance hours per day
- Static file serving: Free bandwidth quota
- Beyond free tier: ~$0.05/hour per instance

**Typical console usage**: Should stay within free tier for small teams.

**Cost optimization**:
```yaml
# Add to app.yaml for auto-scaling limits
automatic_scaling:
  max_instances: 5
  min_instances: 0
  target_cpu_utilization: 0.65
```

## Security Best Practices

1. **Never commit `.env.production.local`**
   - Already in `.gitignore`
   - Contains production secrets

2. **Use different WorkOS credentials** for dev vs prod

3. **Enable HTTPS only**:
   - App Engine enforces HTTPS by default

4. **Review IAM permissions**:
   ```bash
   gcloud app services get-iam-policy console
   ```

5. **Set up Cloud Armor** (optional, for DDoS protection):
   - Cloud Console → Network Security → Cloud Armor

## Monitoring & Alerts

### Set Up Error Alerts

```bash
# Create alert for 4xx/5xx errors
gcloud alpha monitoring policies create \
  --notification-channels=CHANNEL_ID \
  --display-name="Console Errors" \
  --condition-threshold-value=10 \
  --condition-threshold-duration=300s \
  --condition-display-name="HTTP Errors" \
  --aggregation-alignment-period=60s
```

### View Metrics

- Cloud Console → App Engine → Services → console
- View requests, latency, errors, instance hours

## CI/CD Integration

### GitHub Actions Example

Create `.github/workflows/deploy-console.yml`:

```yaml
name: Deploy Console

on:
  push:
    branches: [main]
    paths:
      - 'frontend/console/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - uses: actions/setup-node@v3
        with:
          node-version: '24'

      - name: Install dependencies
        working-directory: frontend/console
        run: npm ci

      - name: Create production env
        working-directory: frontend/console
        run: |
          echo "${{ secrets.ENV_PRODUCTION }}" > .env.production.local

      - id: 'auth'
        uses: 'google-github-actions/auth@v1'
        with:
          credentials_json: '${{ secrets.GCP_SA_KEY }}'

      - name: 'Deploy to App Engine'
        working-directory: frontend/console
        run: npm run deploy
```

## Additional Resources

- [App Engine Documentation](https://cloud.google.com/appengine/docs)
- [App Engine Pricing](https://cloud.google.com/appengine/pricing)
- [WorkOS Documentation](https://workos.com/docs)
- [Vite Production Build](https://vitejs.dev/guide/build.html)

## Support

For issues:
1. Check App Engine logs: `gcloud app logs tail`
2. Check browser console for client errors
3. Verify WorkOS configuration
4. Check environment variables
5. Review this guide's troubleshooting section

---

**Last Updated**: 2025-01-16
