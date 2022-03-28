provider "google" {
  project = var.project
  region  = var.region
}

resource "google_app_engine_application" "app" {
  project       = var.project
  location_id   = var.location_id
  database_type = "CLOUD_FIRESTORE"
}

resource "google_storage_bucket" "bucket" {
  name     = "${var.project}-bucket"
  location = "US"
}

module "access_token" {
    source     = "./modules/secret"
    acessor    = module.croatianbot.service_account_email
    id         = "twitter_access_token"
    value      = "${var.access_token}"
}

module "croatianbot" {
  source               = "./modules/function"
  project              = var.project
  function_name        = "croatianbot"
  function_entry_point = "app"
  pubsub_topic_name    = "croatianbot_trigger"
  source_bucket_name   = google_storage_bucket.bucket.name
  source_dir           = abspath("../python/croatianbot")
  timeout              = 540 # 9 minutes
  depends_on = [
    google_app_engine_application.app,
  ]
}

resource "google_cloud_scheduler_job" "croatianbot_job" {
  name        = "croatianbot_job"
  description = "triggers croatianbot every hour"
  schedule    = "15 * * * *"

  pubsub_target {
    topic_name = "projects/${var.project}/topics/croatianbot_trigger"
    data       = base64encode("test")
  }
  depends_on = [
    module.access_token,
    module.croatianbot,
  ]
}