# model/utils_model.py
from http.client import HTTPException
import json
import logging
import os
import psycopg2
from sqlalchemy.ext.declarative import declarative_base
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the SQLAlchemy Declarative Base
Base = declarative_base()

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.environ["DB_HOST"],
            dbname=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            port=os.environ["DB_PORT"],
        )
        logger.info("Connection to DB established.")
        return conn
    except Exception as e:
        logger.error(f"Error connecting to DB: {str(e)}")
        raise e
