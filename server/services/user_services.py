# services/user_services.py
import os
import logging
import bcrypt  # type: ignore
import jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from model.user_model import User
from pydantic import BaseModel
from model.utils_model import get_db_connection
logger = logging.getLogger(__name__)

SECRET_KEY = os.getenv("SECRET_KEY", "Android@123")
JWT_EXPIRATION_TIME = 60

router = APIRouter()

class SignInRequest(BaseModel):
    identifier: str  # Can be either email or username
    password: str

@router.post("/signin")
def sign_in(sign_in_request: SignInRequest):
    identifier = sign_in_request.identifier
    password = sign_in_request.password

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            SELECT id, employeeId, username, email, birthday, password, created_at, updated_at, deleted_at 
            FROM aslan_users 
            WHERE email = %s OR username = %s
        ''', (identifier, identifier))
        user_row = cursor.fetchone()

        if not user_row:
            return JSONResponse(status_code=401, content={"statusCode": 401, "body": "Unauthorized"})

        stored_password_hash = user_row[5]
        if not bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
            return JSONResponse(status_code=401, content={"statusCode": 401, "body": "Unauthorized"})

        payload = {
            "sub": str(user_row[0]),  # User ID as string
            "exp": datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_TIME)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        user_info = {
            "id": user_row[0],
            "employeeId": user_row[1],
            "username": user_row[2],
            "email": user_row[3],
            "birthday": user_row[4].strftime('%Y-%m-%d') if user_row[4] else None,
            "created_at": user_row[6].strftime('%Y-%m-%d %H:%M:%S') if user_row[6] else None,
            "updated_at": user_row[7].strftime('%Y-%m-%d %H:%M:%S') if user_row[7] else None,
            "deleted_at": user_row[8].strftime('%Y-%m-%d %H:%M:%S') if user_row[8] else None,
            "token": token
        }

        return JSONResponse(status_code=200, content={"statusCode": 200, "body": user_info})

    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    finally:
        cursor.close()
        conn.close()

@router.post("/signout")
def sign_out():
    return JSONResponse(status_code=200, content={"statusCode": 200, "body": "Signed out successfully"})


class RegisterRequest(BaseModel):
    email: str
    username: str
    password: str
    birthday: str


@router.post("/register")
def register(register_request: RegisterRequest):
    email = register_request.email
    username = register_request.username
    password = register_request.password
    birthday = register_request.birthday

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO aslan_users (email, username, password, birthday) 
            VALUES (%s, %s, %s, %s) RETURNING id, employeeId, username, email, birthday, created_at, updated_at, deleted_at
        ''', (email, username, hashed_password, birthday))

        user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=500, detail="Failed to create user")

        user_id = user[0]

        month_start_date = datetime.utcnow()
        month_end_date = month_start_date + timedelta(days=30)

        cursor.execute('''
            INSERT INTO aslan_user_token_usage (user_id, monthly_token_limit, tokens_used, month_start_date, month_end_date, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        ''', (user_id, 1000, 0, month_start_date, month_end_date))

        conn.commit()

        user_info = {
            "id": user[0],
            "employeeId": user[1],
            "username": user[2],
            "email": user[3],
            "birthday": user[4].strftime('%Y-%m-%d') if user[4] else None,
            "created_at": user[5].strftime('%Y-%m-%d %H:%M:%S') if user[5] else None,
            "updated_at": user[6].strftime('%Y-%m-%d %H:%M:%S') if user[6] else None,
            "deleted_at": user[7].strftime('%Y-%m-%d %H:%M:%S') if user[7] else None,
        }

        return JSONResponse(status_code=200, content={
            "statusCode": 200,
            "body": "Registered successfully",
            "user": user_info
        })

    except Exception as e:
        conn.rollback()
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Something went wrong")

    finally:
        cursor.close()
        conn.close()

@router.get("/token-usage/{user_id}")
def get_token_usage(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    with cursor() as cursor:
        cursor.execute('''
            SELECT id, user_id, monthly_token_limit, tokens_used, month_start_date, month_end_date, created_at, updated_at
            FROM aslan_user_token_usage
            WHERE user_id = %s
        ''', (user_id,))
        token_usage = cursor.fetchone()

    if not token_usage:
        raise HTTPException(status_code=404, detail="Token usage record not found")

    return {
        "id": token_usage[0],
        "user_id": token_usage[1],
        "monthly_token_limit": token_usage[2],
        "tokens_used": token_usage[3],
        "month_start_date": token_usage[4].strftime('%Y-%m-%d') if token_usage[4] else None,
        "month_end_date": token_usage[5].strftime('%Y-%m-%d') if token_usage[5] else None,
        "created_at": token_usage[6].strftime('%Y-%m-%d %H:%M:%S') if token_usage[6] else None,
        "updated_at": token_usage[7].strftime('%Y-%m-%d %H:%M:%S') if token_usage[7] else None,
    }

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.put("/token-usage/{user_id}")
def update_token_usage(user_id: int, tokens_used: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    with cursor() as cursor:
        # Fetch current token usage
        cursor.execute('''
            SELECT id, tokens_used, monthly_token_limit
            FROM aslan_user_token_usage
            WHERE user_id = %s
        ''', (user_id,))
        token_usage = cursor.fetchone()

        if not token_usage:
            raise HTTPException(status_code=404, detail="Token usage record not found")

        current_tokens_used = token_usage[1]
        monthly_limit = token_usage[2]

        # Check if the new usage exceeds the limit
        if current_tokens_used + tokens_used > monthly_limit:
            raise HTTPException(status_code=400, detail="Token usage exceeds monthly limit")

        # Update token usage
        updated_tokens_used = current_tokens_used + tokens_used
        cursor.execute('''
            UPDATE aslan_user_token_usage
            SET tokens_used = %s, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = %s
        ''', (updated_tokens_used, user_id))
        cursor.commit()

    return {"message": "Token usage updated successfully", "tokens_used": updated_tokens_used}

@router.get("/user-info")
def get_user_info(token: str = Depends(oauth2_scheme), conn = Depends(get_db_connection)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token: User ID not found")

        with conn.cursor() as cursor:
            # Fetch user details
            cursor.execute('''
                SELECT id, employeeId, username, email, birthday, created_at, updated_at, deleted_at
                FROM aslan_users
                WHERE id = %s
            ''', (user_id,))
            user = cursor.fetchone()

            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            # Fetch token usage
            cursor.execute('''
                SELECT monthly_token_limit, tokens_used
                FROM aslan_user_token_usage
                WHERE user_id = %s
            ''', (user[0],))
            token_usage = cursor.fetchone()

            # Fetch rewards
            cursor.execute('''
                SELECT id, reward_type, reward_description, granted_at
                FROM aslan_rewards
                WHERE user_id = %s
            ''', (user[0],))
            rewards = cursor.fetchall()

        # Construct user info response
        user_info = {
            "id": user[0],
            "employeeId": user[1],
            "username": user[2],
            "email": user[3],
            "birthday": user[4].strftime('%Y-%m-%d') if user[4] else None,
            "created_at": user[5].strftime('%Y-%m-%d %H:%M:%S') if user[5] else None,
            "updated_at": user[6].strftime('%Y-%m-%d %H:%M:%S') if user[6] else None,
            "deleted_at": user[7].strftime('%Y-%m-%d %H:%M:%S') if user[7] else None,
            "token_usage": {
                "monthly_token_limit": token_usage[0] if token_usage else 0,
                "tokens_used": token_usage[1] if token_usage else 0,
            } if token_usage else None,
            "rewards": [
                {
                    "id": reward[0],
                    "reward_type": reward[1],
                    "reward_description": reward[2],
                    "granted_at": reward[3].strftime('%Y-%m-%d %H:%M:%S') if reward[3] else None,
                }
                for reward in rewards
            ],
        }

        return {"statusCode": 200, "body": user_info}

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        logger.error(f"Error fetching user info: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching user info")