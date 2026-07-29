from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.utils.jwt_handler import verify_access_token

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    try:

        payload = verify_access_token(token)

        return payload



    except Exception as e: 
        print("JWT ERROR:", e)

        raise HTTPException(
            status_code=401,
            detail=str(e)
        )