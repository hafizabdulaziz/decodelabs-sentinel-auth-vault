from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
        # Allow documentation paths to load Swagger and Scalar UI assets
        if request.url.path in ["/docs", "/scalar", "/redoc", "/openapi.json", "/"]:
            response.headers["Content-Security-Policy"] = (
                "default-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fastapi.tiangolo.com https://cdn.scalar.com; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://cdn.scalar.com; "
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdn.scalar.com https://fonts.googleapis.com; "
                "img-src 'self' data: https://fastapi.tiangolo.com https://cdn.scalar.com; "
                "font-src 'self' https://fonts.gstatic.com data:;"
            )
        else:
            response.headers["Content-Security-Policy"] = "default-src 'self'"
        return response
