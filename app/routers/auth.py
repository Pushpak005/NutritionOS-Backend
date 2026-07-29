from fastapi import APIRouter, Depends
from sqlalchemy import text

from app.database import engine
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse
)

from app.utils.password import (
    hash_password,
    verify_password
)

from app.utils.jwt_handler import create_access_token
from app.utils.auth_dependency import get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# ==========================================
# Register
# ==========================================

@router.post("/register")
def register(user: RegisterRequest):

    hashed_password = hash_password(user.password)

    with engine.begin() as conn:

        existing_user = conn.execute(
            text("""
                SELECT id
                FROM users
                WHERE email = :email
            """),
            {
                "email": user.email
            }
        ).fetchone()

        if existing_user:
            return {
                "success": False,
                "message": "Email already registered."
            }

        conn.execute(
            text("""
                INSERT INTO users
                (
                    name,
                    email,
                    password_hash
                )
                VALUES
                (
                    :name,
                    :email,
                    :password_hash
                )
            """),
            {
                "name": user.name,
                "email": user.email,
                "password_hash": hashed_password
            }
        )

    return {
        "success": True,
        "message": "User registered successfully."
    }


# ==========================================
# Login
# ==========================================

@router.post("/login", response_model=TokenResponse)
def login(user: LoginRequest):
    print("LOGIN EMAIL RECEIVED:", user.email)

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT
                    id,
                    email,
                    password_hash
                FROM users
                WHERE email = :email
            """),
            {
                "email": user.email
            }
        ).fetchone()

    print("\n==============================")
    print("DB RESULT:", result)
    print("==============================")

    if result is None:
        print("❌ USER NOT FOUND")

        return {
            "access_token": "",
            "token_type": "bearer"
        }

    db_user = dict(result._mapping)

    print("DB USER:", db_user)

    password_ok = verify_password(
        user.password,
        db_user["password_hash"]
    )

    print("PASSWORD OK:", password_ok)

    if not password_ok:
        print("❌ PASSWORD MISMATCH")

        return {
            "access_token": "",
            "token_type": "bearer"
        }

    token = create_access_token(
        {
            "user_id": db_user["id"],
            "email": db_user["email"]
        }
    )

    print("✅ GENERATED TOKEN:", token)

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# ==========================================
# Current User
# ==========================================

@router.get("/me")
def get_me(current_user=Depends(get_current_user)):

    return {
        "message": "Token verified successfully.",
        "user": current_user
    }