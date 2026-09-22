from fastapi import APIRouter
from app.core.responses import api_response

router = APIRouter()

@router.get("/health")
async def health_check():
    return api_response(status="success", data={"status": "ok"})
