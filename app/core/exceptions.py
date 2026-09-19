from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app.core.responses import api_response

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(401)
    async def unauthorized_exception_handler(request: Request, exc):
        return api_response(status="error", message="Unauthorized", data=None)

    @app.exception_handler(422)
    async def validation_exception_handler(request: Request, exc):
        return api_response(status="error", message="Unprocessable Entity", data=exc.errors())
