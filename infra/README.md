# Infrastructure

This directory contains infrastructure-related files and configurations.

## GCS Bucket Examples

Upload files to Google Cloud Storage bucket:

```bash
# Upload robots.txt with cache control
gsutil -m -h "Cache-Control:public, max-age=2592000" cp robots.txt gs://your-bucket-name/seo/robots.txt

# Sync favicon directory
gsutil -m -h "Cache-Control:public, max-age=2592000" rsync favicon/ gs://your-bucket-name/favicon/
```

Replace `your-bucket-name` with your actual GCS bucket name.
