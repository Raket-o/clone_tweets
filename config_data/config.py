"""The config module for checking whether the environment has been created."""
import os

from dotenv import find_dotenv, load_dotenv

if not find_dotenv():
    exit("Environment variables are not loaded because there is no .env file")
else:
    load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
try:
    DB_PORT = int(os.getenv("DB_PORT"))
except ValueError:
    print("DB_PORT != INT")
    exit(1)
DB_NAME = "tweet_clone"
DB_FILLING = os.getenv("DB_FILLING")
DB_TESTS = bool(os.getenv("DB_TESTS"))
