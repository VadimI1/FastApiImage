import os

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(__file__)

load_dotenv(os.path.join(BASE_DIR, '.env'))

DB_HOST=os.environ['DB_HOST']
DB_PORT=os.environ['DB_PORT']
DB_NAME=os.environ['DB_NAME']
DB_USER=os.environ['DB_USER']
DB_PASS=os.environ['DB_PASS']