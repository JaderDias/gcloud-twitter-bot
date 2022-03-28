from Logger import logger

import json
import requests

def post(\
        access_token: str, \
        text:str) -> None:
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