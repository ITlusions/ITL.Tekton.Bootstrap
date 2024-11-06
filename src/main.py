from fastapi import FastAPI
from routers.job_router import router as job_router
from config.settings import settings

app = FastAPI(docs_url=f"{settings.prefix}/docs", openapi_url=f"{settings.prefix}/openapi.json")

app.include_router(job_router)

if __name__ == "__main__":
    import uvicorn
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    uvicorn.run(app, host="0.0.0.0", port=8000, proxy_headers=True, log_config=log_config, forwarded_allow_ips='*')