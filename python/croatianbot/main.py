import Content
from Logger import logger
import Secrets
import Twitter

from datetime import datetime, timedelta

def get_updater() -> None:
    text = Content.get()
    logger.info(text)
    client_id = Secrets.access_secret_version('twitter_client_id')
    client_secret = Secrets.access_secret_version('twitter_client_secret')
    refresh_token = Secrets.access_secret_version('twitter_refresh_token')
    refresh_token = Twitter.post(client_id, client_secret, refresh_token, text)
    Secrets.add_secret_version('twitter_refresh_token', refresh_token)

def app(event, context):
    get_updater()

if __name__ == '__main__':
    get_updater()