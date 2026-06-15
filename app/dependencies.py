from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.auth import verify_token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_user(
        token: str = Depends(oauth2_scheme)
):

    payload = verify_token(token)

    return payload


def admin_required(
        current_user=Depends(get_current_user)
):

    if current_user["role"] != "admin":

        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return current_user