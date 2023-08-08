from dotenv import load_dotenv
import os

load_dotenv()

SERVICE_URL = os.getenv('SERVICE_URL')
REDIRECT_URL = os.getenv('REDIRECT_URL')

DB_URL = os.getenv('DB_URL')
REDIS_URL = os.getenv('REDIS_URL')

RESET_TOKEN = os.environ.get('RESET_TOKEN')
VERIFICATION_TOKEN = os.environ.get('VERIFICATION_TOKEN')

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
BASE_SPOTIFY_TOKEN = os.getenv('BASE_SPOTIFY_TOKEN')


