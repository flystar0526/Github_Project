import os
import secrets
from urllib.parse import quote_plus  # Used for URL encoding
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Application secret key
    SECRET_KEY = secrets.token_hex(16)  # Randomly generated key
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Google Cloud Storage configuration
    GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME')
    GCS_KEY_FILE = os.getenv('GCS_KEY_FILE')  # Service account key file

    # Database configuration
    DB_USER = os.getenv('DB_USER')  # Username
    DB_PASSWORD = quote_plus(os.getenv('DB_PASSWORD'))  # URL encoded password
    DB_NAME = os.getenv('DB_NAME')  # Database name
    DB_HOST = os.getenv('DB_HOST')  # Cloud SQL public IP
    DB_PORT = os.getenv('DB_PORT', '5432')  # Default PostgreSQL port

    # Database URI
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
