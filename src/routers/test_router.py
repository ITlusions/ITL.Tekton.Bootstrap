import logging
from fastapi import APIRouter, HTTPException, Request, Depends
from models.job_model import JobSpec
#from controllers.job_controller import create_job
from config.settings import settings
from base.auth import get_api_key

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.get("/test")
async def test_api(request: Request):
    headers = dict(request.headers)
    
    # Extract the client's IP from the "X-Forwarded-For" header, if available
    # To get this working, set externalTrafficPolicy: Local
    x_forwarded_for = headers.get("x-forwarded-for")
    client_ip = x_forwarded_for.split(",")[0] if x_forwarded_for else request.client.host
    
    # Log the client's IP to the console
    logger.info(f"Client IP: {client_ip}")
    
    return headers