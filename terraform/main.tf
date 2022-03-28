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

module "client_id" {
    source     = "./modules/secret"
    acessor    = module.croatianbot.service_account_email
    id         = "twitter_client_id"
    value      = "${var.client_id}"
    depends_on = [
        module.croatianbot,
    ]
}

module "client_secret" {
    source     = "./modules/secret"
    acessor    = module.croatianbot.service_account_email
    id         = "twitter_client_secret"
    value      = "${var.client_secret}"
    depends_on = [
        module.croatianbot,
    ]
}

module "refresh_token" {
    source     = "./modules/secret"
    acessor    = module.croatianbot.service_account_email
    id         = "twitter_refresh_token"
    value      = "${var.refresh_token}"
    depends_on = [
        module.croatianbot,
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
    module.client_id,
    module.client_secret,
    module.refresh_token,
  ]
}