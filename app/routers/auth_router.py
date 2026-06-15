from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database import get_db

from app.models import User

from app.schemas import UserCreate
from app.schemas import LoginRequest

from app.auth import hash_password
from app.auth import verify_password
from app.auth import create_access_token
from app.auth import create_refresh_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
        user: UserCreate,
        db: Session = Depends(get_db)
):

    db_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(db_user)

    db.commit()

    return {
        "message": "User registered"
    }


@router.post("/login")
def login(
        request: LoginRequest,
        db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == request.username
    ).first()

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
            request.password,
            user.password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    access_token = create_access_token({
        "sub": user.username,
        "role": user.role
    })

    refresh_token = create_refresh_token({
        "sub": user.username
    })

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }