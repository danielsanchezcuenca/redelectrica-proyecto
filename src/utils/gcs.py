import json
from google.cloud import storage


def upload_json(bucket_name: str, blob_path: str, data: dict) -> str:
    """ Sube un dict como JSON a GCS y devuelve el URI gs://... """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_path)
    blob.cache_control = "no-cache"
    blob.upload_from_string(
        json.dumps(data, ensure_ascii = False),
        content_type = "application/json"
    )
    return f"gs://{bucket_name}/{blob_path}"

def upload_text (bucket_name: str, blob_path: str, data: dict, text:str) -> str:
    """  Sube texto plano a GCS  """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_path)
    blob.upload_from_string(text, content_type = "text/plain; charset=utf-8")
    return f"gs://{bucket_name}/{blob_path}"