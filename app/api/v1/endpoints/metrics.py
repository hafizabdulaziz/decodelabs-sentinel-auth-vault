from fastapi import APIRouter, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest

router = APIRouter()

REQUEST_COUNT = Counter("http_requests_total", "Total HTTP Requests")

@router.get("/metrics")
async def metrics():
    REQUEST_COUNT.inc()
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
