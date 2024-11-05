import logging
from fastapi import APIRouter, HTTPException, Request, Depends
from models.job_model import JobSpec
from controllers.job_controller import create_job
from config.settings import settings
from base.auth import get_api_key

router = APIRouter(prefix=settings.prefix)

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

@router.post("/bootstrap")
async def trigger_job(request: Request, api_key: str = Depends(get_api_key)):
    event_type = request.headers.get("X-GitHub-Event")
    if event_type != "repository":
        raise HTTPException(status_code=400, detail="Invalid event type")

    payload = await request.json()

    if payload.get("action") == "created":
        try:
            job_name = "tkn-bootstrap-repo-job"
            repo_url = payload.get("repository", {}).get("clone_url")
            if not repo_url:
                raise HTTPException(status_code=400, detail="Repository URL not found in payload")
            
            job_spec = JobSpec(name=job_name, repo_url=repo_url)
            create_job(job_spec)
            return {"message": "Job created successfully", "job_name": job_name}

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return {"message": "No action taken, not a repository creation event."}
