# Google Cloud Platform Setup Guide

This guide will walk you through setting up your GCP project for deploying the Django-GCP boilerplate.

## Prerequisites

- Google Cloud account
- `gcloud` CLI installed
- Project billing enabled

## 1. Install Google Cloud SDK

```bash
# macOS
brew install --cask google-cloud-sdk

# Or download from: https://cloud.google.com/sdk/docs/install
```

## 2. Create GCP Project

```bash
# Set your project ID (must be globally unique)
export PROJECT_ID="your-project-id"

# Create project
gcloud projects create $PROJECT_ID

# Set as default project
gcloud config set project $PROJECT_ID

# Enable billing (required for Cloud Run, Cloud SQL, etc.)
# Visit: https://console.cloud.google.com/billing
```

## 3. Enable Required APIs

```bash
# Enable all required GCP APIs
gcloud services enable \
  run.googleapis.com \
  sqladmin.googleapis.com \
  storage-api.googleapis.com \
  cloudtasks.googleapis.com \
  cloudbuild.googleapis.com \
  secretmanager.googleapis.com \
  vpcaccess.googleapis.com \
  logging.googleapis.com
```

## 4. Create Service Account

```bash
# Create service account for the application
gcloud iam service-accounts create django-app \
  --display-name="Django Application Service Account"

# Grant necessary permissions
export SERVICE_ACCOUNT="django-app@${PROJECT_ID}.iam.gserviceaccount.com"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${SERVICE_ACCOUNT}" \
  --role="roles/cloudsql.client"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${SERVICE_ACCOUNT}" \
  --role="roles/storage.objectAdmin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${SERVICE_ACCOUNT}" \
  --role="roles/cloudtasks.enqueuer"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${SERVICE_ACCOUNT}" \
  --role="roles/logging.logWriter"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${SERVICE_ACCOUNT}" \
  --role="roles/secretmanager.secretAccessor"
```

## 5. Create Cloud SQL Instance

```bash
# Set region
export REGION="us-central1"

# Create PostgreSQL instance
gcloud sql instances create django-db \
  --database-version=POSTGRES_16 \
  --tier=db-f1-micro \
  --region=$REGION \
  --root-password="YOUR_SECURE_PASSWORD"

# Create database
gcloud sql databases create django_db \
  --instance=django-db

# Create database user
gcloud sql users create django_user \
  --instance=django-db \
  --password="YOUR_SECURE_PASSWORD"
```

## 6. Create Cloud Storage Bucket

```bash
# Create bucket for static/media files
export BUCKET_NAME="${PROJECT_ID}-static"

gsutil mb -p $PROJECT_ID -l $REGION gs://$BUCKET_NAME

# Make bucket publicly readable (for static files)
gsutil iam ch allUsers:objectViewer gs://$BUCKET_NAME

# Set CORS policy (if needed for media uploads)
echo '[{"origin": ["*"], "method": ["GET", "HEAD"], "responseHeader": ["Content-Type"], "maxAgeSeconds": 3600}]' > cors.json
gsutil cors set cors.json gs://$BUCKET_NAME
rm cors.json
```

## 7. Create VPC Connector (for Cloud SQL private IP)

```bash
# Create VPC connector
gcloud compute networks vpc-access connectors create django-connector \
  --region=$REGION \
  --range=10.8.0.0/28
```

## 8. Create Artifact Registry Repository

```bash
# Create repository for Docker images
gcloud artifacts repositories create deploy \
  --repository-format=docker \
  --location=$REGION \
  --description="Django app Docker images"

# Configure Docker authentication
gcloud auth configure-docker ${REGION}-docker.pkg.dev
```

## 9. Store Secrets in Secret Manager

```bash
# Django secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())" | \
  gcloud secrets create SECRET_KEY --data-file=-

# Database password
echo -n "YOUR_DB_PASSWORD" | gcloud secrets create POSTGRES_PASSWORD --data-file=-

# Database host (Cloud SQL private IP)
gcloud sql instances describe django-db --format='value(ipAddresses[0].ipAddress)' | \
  gcloud secrets create POSTGRES_HOST --data-file=-

# Firebase credentials (see FIREBASE_SETUP.md)
echo -n "BASE64_ENCODED_FIREBASE_CREDS" | gcloud secrets create FIREBASE_AUTH_CREDS_HASH --data-file=-

# Grant service account access to secrets
for secret in SECRET_KEY POSTGRES_PASSWORD POSTGRES_HOST FIREBASE_AUTH_CREDS_HASH; do
  gcloud secrets add-iam-policy-binding $secret \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role="roles/secretmanager.secretAccessor"
done
```

## 10. Configure gcloud CLI

```bash
# Create named configuration
gcloud config configurations create django-gcp

# Activate configuration
gcloud config configurations activate django-gcp

# Set project
gcloud config set project $PROJECT_ID

# Set region
gcloud config set run/region $REGION

# Set account
gcloud config set account YOUR_EMAIL@example.com
```

## 11. Update Deployment Files

Update `backend/core/deploy/core.yaml`:

```yaml
image: us-central1-docker.pkg.dev/YOUR_PROJECT_ID/deploy/core
service-account: django-app@YOUR_PROJECT_ID.iam.gserviceaccount.com
vpc-connector: projects/YOUR_PROJECT_ID/locations/us-central1/connectors/django-connector
region: us-central1
add-cloudsql-instances: YOUR_PROJECT_ID:us-central1:django-db
```

Update `backend/core/deploy/cloudbuild.yaml`:

Replace `PROJECT_ID` with your actual project ID, or use substitutions.

## Summary Checklist

- [ ] GCP project created
- [ ] Billing enabled
- [ ] Required APIs enabled
- [ ] Service account created with permissions
- [ ] Cloud SQL instance created
- [ ] Cloud Storage bucket created
- [ ] VPC connector created
- [ ] Artifact Registry repository created
- [ ] Secrets stored in Secret Manager
- [ ] gcloud CLI configured
- [ ] Deployment files updated

## Next Steps

- Configure Firebase (see [FIREBASE_SETUP.md](FIREBASE_SETUP.md))
- Deploy application (see [DEPLOYMENT.md](DEPLOYMENT.md))

## Cost Optimization Tips

- Use `db-f1-micro` or `db-g1-small` for Cloud SQL in development
- Set Cloud Run min-instances to 0 for development
- Use Cloud Storage lifecycle policies to delete old logs
- Monitor usage with Cloud Billing reports

## Troubleshooting

### Permission Denied Errors

Ensure service account has all required roles:
```bash
gcloud projects get-iam-policy $PROJECT_ID \
  --flatten="bindings[].members" \
  --filter="bindings.members:serviceAccount:${SERVICE_ACCOUNT}"
```

### Cloud SQL Connection Issues

Check VPC connector is created:
```bash
gcloud compute networks vpc-access connectors describe django-connector \
  --region=$REGION
```

### Docker Push Fails

Re-authenticate Docker:
```bash
gcloud auth configure-docker ${REGION}-docker.pkg.dev
```
