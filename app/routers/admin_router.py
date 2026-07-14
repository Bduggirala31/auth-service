from fastapi import APIRouter
from fastapi import Depends

from app.dependencies import admin_required

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/dashboard")
def dashboard(
        current_user=Depends(
            admin_required
        )
):

    return {
        "message": "Admin dashboard"
    }