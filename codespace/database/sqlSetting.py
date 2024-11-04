from sqlalchemy import create_engine

import os
from dotenv import load_dotenv

load_dotenv()

class Engine:
    engine:create_engine
    def __init__(self) -> None:
        db = {
            'user': os.getenv("DB_USER"),
            'password': os.getenv("DB_PASSWORD"),
            'host': os.getenv("DB_HOST"),
            'port': os.getenv("DB_PORT"),
            'database': os.getenv("DB_DATABASE")
        }
        db_url = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"
        self.engine = create_engine(db_url)