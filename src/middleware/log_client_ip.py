from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import logging

logger = logging.getLogger("uvicorn.access")

class ClientIPLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        logger = logging.getLogger("uvicorn.access")
        logger = logging.LoggerAdapter(logger, {"client_addr": client_ip})
        logger.info(f"Client IP: {client_ip}")
        response = await call_next(request)
        return response