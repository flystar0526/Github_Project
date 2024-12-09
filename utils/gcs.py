from google.cloud import storage
import os
from uuid import uuid4

class GCSHelper:
  def __init__(self, bucket_name):
    self.bucket_name = bucket_name
    self.client = storage.Client()
    self.bucket = self.client.bucket(bucket_name)

  def upload_file(self, file, folder):
    filename = f"{folder}/{uuid4().hex}{os.path.splitext(file.filename)[1]}"
    blob = self.bucket.blob(filename)
    blob.upload_from_file(file, content_type=file.content_type)
    return f"https://storage.googleapis.com/{self.bucket_name}/{filename}"

# Initialize GCS helper
gcs_helper = GCSHelper(bucket_name=os.getenv('GCS_BUCKET_NAME'))
