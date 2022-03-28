import base64
import hashlib
import subprocess
import os
from os.path import exists
import re
import json
import requests
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

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

access_token = get_secret("twitter_access_token")
if not access_token:
    client_id = input("Enter Twitter API Client Id: ")
    client_secret = input("Enter Twitter API Client Secret: ")

    # Replace the following URL with your callback URL, which can be obtained from your App's auth settings.
    redirect_uri = "https://github.com/JaderDias"

    # Set the scopes
    scopes = ["bookmark.read", "tweet.read", "tweet.write", "users.read", "offline.access"]

    # Create a code verifier
    code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8")
    code_verifier = re.sub("[^a-zA-Z0-9]+", "", code_verifier)

    # Create a code challenge
    code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
    code_challenge = code_challenge.replace("=", "")

    # Start an OAuth 2.0 session
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scopes)

    # Create an authorize URL
    auth_url = "https://twitter.com/i/oauth2/authorize"
    authorization_url, state = oauth.authorization_url(
        auth_url, code_challenge=code_challenge, code_challenge_method="S256"
    )

    # Visit the URL to authorize your App to make requests on behalf of a user
    print(
        "Visit the following URL to authorize your App on behalf of your Twitter handle in a browser:"
    )
    print(authorization_url)

    # Paste in your authorize URL to complete the request
    authorization_response = input(
        "Paste in the full URL after you've authorized your App:\n"
    )

    # Fetch your access token
    token_url = "https://api.twitter.com/2/oauth2/token"

    auth = HTTPBasicAuth(client_id, client_secret)

    token = oauth.fetch_token(
        token_url=token_url,
        authorization_response=authorization_response,
        auth=auth,
        client_id=client_id,
        include_client_id=True,
        code_verifier=code_verifier,
    )

    # Your access token
    access_token = token["access_token"]

os.chdir('terraform')
run_cmd("terraform init")
run_cmd(f"""terraform apply
    --var project={project_id}
    --var access_token={access_token}
""")