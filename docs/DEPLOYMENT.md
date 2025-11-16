# Deployment Guide

This guide covers deploying the Django-GCP boilerplate to Google Cloud Run.

## Prerequisites

- Completed [GCP Setup](GCP_SETUP.md)
- Configured [Firebase Authentication](FIREBASE_SETUP.md)
- Docker installed locally
- gcloud CLI configured

## Deployment Methods

### Method 1: Using Django Management Command (Recommended)

The boilerplate includes custom Django management commands for easy deployment.

```bash
cd backend/core

# Deploy to production
python manage.py deploy

# Deploy beta version (no traffic)
python manage.py deploy --beta

# Dry run (see commands without executing)
python manage.py deploy --dry-run

# Use Cloud Build for building images
python manage.py deploy --use_cloud_build
```

### Method 2: Manual Deployment

#### Step 1: Build Docker Image

```bash
cd backend/core

# Build the image
docker build -t ${REGION}-docker.pkg.dev/${PROJECT_ID}/deploy/core .

# Push to Artifact Registry
docker push ${REGION}-docker.pkg.dev/${PROJECT_ID}/deploy/core
```

#### Step 2: Deploy to Cloud Run

```bash
# Deploy with gcloud
gcloud run deploy core \
  --image=${REGION}-docker.pkg.dev/${PROJECT_ID}/deploy/core \
  --platform=managed \
  --region=${REGION} \
  --allow-unauthenticated \
  --service-account=django-app@${PROJECT_ID}.iam.gserviceaccount.com \
  --vpc-connector=django-connector \
  --add-cloudsql-instances=${PROJECT_ID}:${REGION}:django-db \
  --set-secrets=SECRET_KEY=SECRET_KEY:latest,POSTGRES_PASSWORD=POSTGRES_PASSWORD:latest,POSTGRES_HOST=POSTGRES_HOST:latest,FIREBASE_AUTH_CREDS_HASH=FIREBASE_AUTH_CREDS_HASH:latest \
  --set-env-vars=ENV=prod,GCP_PROJECT_ID=${PROJECT_ID},GCP_REGION=${REGION} \
  --timeout=60s \
  --concurrency=50 \
  --min-instances=0 \
  --max-instances=10 \
  --cpu=1 \
  --memory=4G
```

## First-Time Deployment

### 1. Update Configuration Files

Edit `backend/core/deploy/core.yaml`:

```yaml
image: us-central1-docker.pkg.dev/YOUR_PROJECT_ID/deploy/core
service-account: django-app@YOUR_PROJECT_ID.iam.gserviceaccount.com
vpc-connector: projects/YOUR_PROJECT_ID/locations/us-central1/connectors/django-connector
region: us-central1
add-cloudsql-instances: YOUR_PROJECT_ID:us-central1:django-db
```

### 2. Run Database Migrations

After first deployment, run migrations on Cloud Run:

```bash
# Option 1: Using Cloud Run jobs (recommended)
gcloud run jobs create migrate \
  --image=${REGION}-docker.pkg.dev/${PROJECT_ID}/deploy/core \
  --region=${REGION} \
  --service-account=django-app@${PROJECT_ID}.iam.gserviceaccount.com \
  --vpc-connector=django-connector \
  --add-cloudsql-instances=${PROJECT_ID}:${REGION}:django-db \
  --set-secrets=SECRET_KEY=SECRET_KEY:latest,POSTGRES_PASSWORD=POSTGRES_PASSWORD:latest,POSTGRES_HOST=POSTGRES_HOST:latest \
  --set-env-vars=ENV=prod,GCP_PROJECT_ID=${PROJECT_ID} \
  --command=python \
  --args=manage.py,migrate

# Execute the job
gcloud run jobs execute migrate --region=${REGION}

# Option 2: Using Cloud Shell with Cloud SQL Proxy
# Connect to Cloud SQL
gcloud sql connect django-db --user=django_user

# In another terminal, run migrations
python manage.py migrate
```

### 3. Create Superuser

```bash
# Create a Cloud Run job for createsuperuser
gcloud run jobs create createsuperuser \
  --image=${REGION}-docker.pkg.dev/${PROJECT_ID}/deploy/core \
  --region=${REGION} \
  --service-account=django-app@${PROJECT_ID}.iam.gserviceaccount.com \
  --vpc-connector=django-connector \
  --add-cloudsql-instances=${PROJECT_ID}:${REGION}:django-db \
  --set-secrets=SECRET_KEY=SECRET_KEY:latest,POSTGRES_PASSWORD=POSTGRES_PASSWORD:latest,POSTGRES_HOST=POSTGRES_HOST:latest \
  --set-env-vars=ENV=prod,GCP_PROJECT_ID=${PROJECT_ID} \
  --command=python \
  --args=manage.py,createsuperuser,--noinput,--email=admin@example.com

# Execute
gcloud run jobs execute createsuperuser --region=${REGION}
```

### 4. Collect Static Files

Static files are automatically collected during the Docker build process.

To manually collect and upload to GCS:

```bash
# Set environment variables
export GCS_BUCKET_NAME=${PROJECT_ID}-static
export USE_GCS=True

# Collect static files
python manage.py collectstatic --noinput
```

## Deploy Cloud Tasks Queues

```bash
cd backend/core
python manage.py deploy_task_queues
```

## Beta Deployments

Deploy a new version without routing traffic (for testing):

```bash
# Deploy beta version
python manage.py deploy --beta

# Test the beta URL
# URL will be: https://beta---core-{hash}.a.run.app

# Once tested, migrate traffic
gcloud run services update-traffic core \
  --to-latest \
  --region=${REGION}
```

## Rolling Back

```bash
# List revisions
gcloud run revisions list --service=core --region=${REGION}

# Route traffic to previous revision
gcloud run services update-traffic core \
  --to-revisions=core-00001-xyz=100 \
  --region=${REGION}
```

## Environment Variables

Set environment variables in Cloud Run:

```bash
gcloud run services update core \
  --update-env-vars=HOST_URL=https://your-domain.com \
  --region=${REGION}
```

## Monitoring

### View Logs

```bash
# View recent logs
gcloud run services logs read core --region=${REGION}

# Tail logs
gcloud run services logs tail core --region=${REGION}

# Or use Cloud Console:
# https://console.cloud.google.com/run?project=YOUR_PROJECT_ID
```

### Metrics

View metrics in Cloud Console:
- https://console.cloud.google.com/run/detail/${REGION}/core/metrics

Key metrics to monitor:
- Request count
- Request latency
- Instance count
- Memory utilization
- CPU utilization

## Custom Domain

### 1. Map Custom Domain

```bash
gcloud run domain-mappings create \
  --service=core \
  --domain=api.yourdomain.com \
  --region=${REGION}
```

### 2. Update DNS

Add the DNS records shown in the output to your domain registrar.

### 3. Update Settings

Update `HOST_URL` in Cloud Run environment variables:

```bash
gcloud run services update core \
  --update-env-vars=HOST_URL=https://api.yourdomain.com \
  --region=${REGION}
```

## CI/CD Integration

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Cloud Run

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - uses: google-github-actions/setup-gcloud@v1
        with:
          service_account_key: ${{ secrets.GCP_SA_KEY }}
          project_id: ${{ secrets.GCP_PROJECT_ID }}

      - name: Configure Docker
        run: gcloud auth configure-docker us-central1-docker.pkg.dev

      - name: Build and Deploy
        run: |
          cd backend/core
          gcloud builds submit --config=deploy/cloudbuild.yaml
          python manage.py deploy
```

## Troubleshooting

### Deployment Fails

Check the build logs:
```bash
gcloud builds list --limit=5
gcloud builds log BUILD_ID
```

### Service Won't Start

Check Cloud Run logs:
```bash
gcloud run services logs read core --region=${REGION} --limit=50
```

### Database Connection Issues

Verify Cloud SQL connection:
```bash
# Check VPC connector
gcloud compute networks vpc-access connectors describe django-connector --region=${REGION}

# Test Cloud SQL connection
gcloud sql connect django-db --user=django_user
```

### Static Files Not Loading

Check GCS bucket permissions:
```bash
gsutil iam get gs://${BUCKET_NAME}
```

## Performance Optimization

### Increase Resources

```bash
gcloud run services update core \
  --cpu=2 \
  --memory=8G \
  --region=${REGION}
```

### Auto-scaling

```bash
gcloud run services update core \
  --min-instances=1 \
  --max-instances=20 \
  --region=${REGION}
```

### Concurrency

```bash
gcloud run services update core \
  --concurrency=100 \
  --region=${REGION}
```

## Cost Optimization

- Set `min-instances=0` for development
- Use smaller machine types for low-traffic apps
- Implement caching (Redis/Memcached)
- Optimize database queries
- Use Cloud CDN for static files

## Security Checklist

- [ ] Secrets stored in Secret Manager (not environment variables)
- [ ] Service account has minimal required permissions
- [ ] VPC connector configured for Cloud SQL private IP
- [ ] HTTPS enforced (Cloud Run default)
- [ ] CORS configured properly
- [ ] Django `DEBUG=False` in production
- [ ] Strong `SECRET_KEY` generated
- [ ] Database credentials rotated regularly
- [ ] Security headers configured

## Next Steps

- Set up monitoring and alerting
- Configure backup strategy for Cloud SQL
- Implement CI/CD pipeline
- Set up staging environment
- Configure CDN for static files
