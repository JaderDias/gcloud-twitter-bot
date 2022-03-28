from google.cloud import secretmanager, storage
import google_crc32c

def access_secret_version(secret_id: str, version_id="latest") -> str:
    # Create the Secret Manager client.
    secretmanager_client = secretmanager.SecretManagerServiceClient()

    storage_client = storage.Client()

    # Build the resource name of the secret version.
    name = f"projects/{storage_client.project}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = secretmanager_client.access_secret_version(name=name)

    # Return the decoded payload.
    return response.payload.data.decode('UTF-8')

def add_secret_version(secret_id: str, payload: str) -> None:
    # Create the Secret Manager client.
    secretmanager_client = secretmanager.SecretManagerServiceClient()

    storage_client = storage.Client()

    # Build the resource name of the secret.
    parent = secretmanager_client.secret_path(storage_client.project, secret_id)

    # Convert the string payload into a bytes. This step can be omitted if you
    # pass in bytes instead of a str for the payload argument.
    payload = payload.encode("UTF-8")

    # Calculate payload checksum. Passing a checksum in add-version request
    # is optional.
    crc32c = google_crc32c.Checksum()
    crc32c.update(payload)

    payload = secretmanager.SecretPayload(
        {"data": payload, "data_crc32c": int(crc32c.hexdigest(), 16)}
    )

    # Add the secret version.
    secretmanager_client.add_secret_version(
        parent=parent,
        payload=payload,
    )