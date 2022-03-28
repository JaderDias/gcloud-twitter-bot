import subprocess
import os
from os.path import exists

from importlib.machinery import SourceFileLoader
  
Logger = SourceFileLoader("Logger","python/croatianbot/Logger.py").load_module()
Twitter = SourceFileLoader("Twitter","python/croatianbot/Twitter.py").load_module()

def run_cmd(bashCommand: str)-> None:
    process = subprocess.Popen(bashCommand.split())
    process.communicate()

def get_result(bashCommand: str) -> str:
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    result, _ = process.communicate()
    return result.decode('ascii').rstrip()

def get_secret(key: str)-> str:
    return get_result(f"gcloud secrets versions access latest --secret={key}")

if exists("terraform/terraform.tfstate"):
    project_id = get_result("jq -r .resources[0].instances[0].attributes.app_id terraform/terraform.tfstate")
    run_cmd(f"gcloud config set project {project_id}")
else:
    print("no terraform state file")
    exit(1)

run_cmd("""gcloud services enable
    appengine.googleapis.com
    cloudbuild.googleapis.com
    cloudfunctions.googleapis.com
    cloudscheduler.googleapis.com
    pubsub.googleapis.com
    secretmanager.googleapis.com
    storage.googleapis.com""")

client_id = get_secret("twitter_client_id")
if not client_id:
    client_id = input("Enter Twitter API Client Id: ")

client_secret = get_secret("twitter_client_secret")
if not client_secret:
    client_secret = input("Enter Twitter API Client Secret: ")

refresh_token = get_secret("twitter_refresh_token")
if not refresh_token:
    # Replace the following URL with your callback URL, which can be obtained from your App's auth settings.
    redirect_uri = "https://github.com/JaderDias"

    token = Twitter.get_token(client_id, client_secret, refresh_token=None)

    # Your access token
    refresh_token = token["refresh_token"]

os.chdir('terraform')
run_cmd("terraform init")
run_cmd(f"""terraform apply
    --var project={project_id}
    --var client_id={client_id}
    --var client_secret={client_secret}
    --var refresh_token={refresh_token}
""")