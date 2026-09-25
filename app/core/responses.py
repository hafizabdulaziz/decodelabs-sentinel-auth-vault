from datetime import datetime
from typing import Any

from fastapi.responses import JSONResponse


def api_response(status: str, data: Any = None, message: str = "") -> JSONResponse:
    return JSONResponse(
        content={
            "status": status,
            "data": data,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
    )
