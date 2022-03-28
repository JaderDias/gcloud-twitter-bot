from google.cloud import secretmanager, storage

def access_secret_version(secret_id, version_id="latest"):
    # Create the Secret Manager client.
    secretmanager_client = secretmanager.SecretManagerServiceClient()

    storage_client = storage.Client()

    # Build the resource name of the secret version.
    name = f"projects/{storage_client.project}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = secretmanager_client.access_secret_version(name=name)

    # Return the decoded payload.
    return response.payload.data.decode('UTF-8')