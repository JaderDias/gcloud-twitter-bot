from Logger import logger

import base64
import hashlib
import json
import os
import re
import requests
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth

def get_token(\
        client_id: str, \
        client_secret: str, \
        refresh_token: str) -> dict:
    # Replace the following URL with your callback URL, which can be obtained from your App's auth settings.
    redirect_uri = "https://github.com/JaderDias"

    # Set the scopes
    scopes = ["bookmark.read", "tweet.read", "tweet.write", "users.read", "offline.access"]

    # Start an OAuth 2.0 session
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scopes)

    token_url = "https://api.twitter.com/2/oauth2/token"
    auth = HTTPBasicAuth(client_id, client_secret)

    if refresh_token:
        return oauth.refresh_token(
            token_url=token_url,
            refresh_token=refresh_token,
            auth=auth,
            client_id=client_id,
            include_client_id=True,
        )

    # Create a code verifier
    code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8")
    code_verifier = re.sub("[^a-zA-Z0-9]+", "", code_verifier)

    # Create a code challenge
    code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
    code_challenge = code_challenge.replace("=", "")

    # Create an authorize URL
    auth_url = "https://twitter.com/i/oauth2/authorize"
    authorization_url, _ = oauth.authorization_url(
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

    return oauth.fetch_token(
        token_url=token_url,
        authorization_response=authorization_response,
        auth=auth,
        client_id=client_id,
        include_client_id=True,
        code_verifier=code_verifier,
    )

def post(\
        client_id: str, \
        client_secret: str, \
        refresh_token: str, \
        text:str) -> str:

    token = get_token(client_id, client_secret, refresh_token)
    access_token = token["access_token"]

    # Be sure to add replace the text of the with the text you wish to Tweet. You can also add parameters to post polls, quote Tweets, Tweet with reply settings, and Tweet to Super Followers in addition to other features.
    payload = {"text": text}

    response = requests.post(
        "https://api.twitter.com/2/tweets",
        headers={"Authorization": "Bearer {}".format(access_token)},
        json=payload
    )

    if response.status_code != 201:
        raise Exception(
            "Request returned an error: {} {}".format(response.status_code, response.text)
        )

    logger.info("Response code: {}".format(response.status_code))

    # Saving the response as JSON
    json_response = response.json()
    logger.info(json.dumps(json_response, indent=4, sort_keys=True))
    return token["refresh_token"]