from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = os.environ.get('DB_URL')
REDIS_URL = os.environ.get('REDIS_URL')
RESET_TOKEN = os.environ.get('RESET_TOKEN')
VERIFICATION_TOKEN = os.environ.get('VERIFICATION_TOKEN')


