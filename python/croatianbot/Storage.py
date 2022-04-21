from Logger import logger

from google.cloud import storage
from datetime import datetime, timedelta

def get_blob(blob_name: str) -> storage.blob:
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(f"{storage_client.project}-bucket")
    return bucket.blob(blob_name)

def read_and_update_published_time() -> bool:
    blob = get_blob('published_time')
    pub_epoch = 0
    if blob.exists():
        pub_epoch = float(blob.download_as_string().decode('ascii'))
    if pub_epoch + 86400 < datetime.now().timestamp():
        blob.upload_from_string(str(datetime.now().timestamp()))
        return True
    return False

def read_pub_count() -> int:
    blob = get_blob('published_count')
    pub_count = 0
    if blob.exists():
        pub_count = int(blob.download_as_string())
    return pub_count

def update_pub_count(new_value: int) -> None:
    blob = get_blob('published_count')
    blob.upload_from_string(str(new_value))