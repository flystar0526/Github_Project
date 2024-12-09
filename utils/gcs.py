from google.cloud import storage
import os
from uuid import uuid4

class GCSHelper:
  def __init__(self, bucket_name, key_file):
    self.bucket_name = bucket_name
    self.client = storage.Client.from_service_account_json(key_file)
    self.bucket = self.client.bucket(bucket_name)

  def upload_file(self, file, folder):
    filename = f"{folder}/{uuid4().hex}{os.path.splitext(file.filename)[1]}"
    blob = self.bucket.blob(filename)
    blob.upload_from_file(file, content_type=file.content_type)
    # 不需要設置 ACL，使用 Bucket 的 IAM 控制
    return f"https://storage.googleapis.com/{self.bucket_name}/{filename}"

# 初始化 GCS 工具
gcs_helper = GCSHelper(
    bucket_name=os.getenv('GCS_BUCKET_NAME'),
    key_file=os.getenv('GCS_KEY_FILE')
)
