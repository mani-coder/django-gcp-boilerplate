provider "google" {
  project = "your-gcp-project-id"
  region  = "us-central1"
}

resource "google_cloud_tasks_queue" "async-tasks-queue" {
  name     = "async-tasks-queue"      # Name of the queue
  location = "us-central1"

  rate_limits {
    max_dispatches_per_second  = 500   # Maximum tasks per second
    max_concurrent_dispatches  = 10    # Maximum concurrent tasks
  }

  retry_config {
    max_attempts    = 5               # Maximum retry attempts
    min_backoff     = "1s"            # Minimum time to wait before retry (ISO 8601 duration)
    max_backoff     = "3600s"         # Maximum time to wait before retry (ISO 8601 duration)
    max_doublings   = 5               # Max retry interval doublings
  }
}

output "queue_name" {
  value = google_cloud_tasks_queue.async-tasks-queue.name
}
