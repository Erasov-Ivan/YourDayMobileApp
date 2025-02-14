import logging
from databaseconnection import DataBaseWorker
from dotenv import load_dotenv
import os
import asyncio
import nest_asyncio
import jwt

nest_asyncio.apply()

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
LOG_FORMAT = os.getenv('LOG_FORMAT')
DATE_FORMAT = os.getenv("DATE_FORMAT")
HASH_KEY = os.getenv("HASH_KEY")


async def encode_jwt_token(data: str) -> str:
    payload = {
        'data': data
    }
    token = jwt.encode(
        payload=payload,
        key=HASH_KEY,
        algorithm='HS256'
    )
    return token


async def decode_jwt_token(token: str) -> str:
    payload = jwt.decode(
        jwt=token,
        key=HASH_KEY,
        algorithms=['HS256']
    )
    try:
        data = payload['data']
        return data
    except KeyError:
        return None


def get_db_connection() -> DataBaseWorker:
    db = DataBaseWorker(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )
    asyncio.run(db.initialize_connection())
    return db


def configure_logging(level: int = logging.INFO) -> None:
    logging.basicConfig(
        level=level,
        format=LOG_FORMAT,
    )
