import Content
from Logger import logger
import Secrets
import Twitter

from datetime import datetime, timedelta

def get_updater() -> None:
    text = Content.get()
    logger.info(text)
    access_token = Secrets.access_secret_version('twitter_access_token')
    Twitter.post(access_token, text)

def app(event, context):
    get_updater()

if __name__ == '__main__':
    get_updater()