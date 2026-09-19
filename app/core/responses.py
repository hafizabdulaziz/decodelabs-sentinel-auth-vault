from typing import Any
from fastapi.responses import JSONResponse
from datetime import datetime

def api_response(status: str, data: Any = None, message: str = "") -> JSONResponse:
    return JSONResponse(
        content={
            "status": status,
            "data": data,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
    )
