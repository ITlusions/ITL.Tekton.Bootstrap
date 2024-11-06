from fastapi import FastAPI
from routers.job_router import router as job_router
from config.settings import settings
from base.logging import setup_logging
from middleware.log_client_ip import ClientIPLoggerMiddleware

log_config = setup_logging()

app = FastAPI(docs_url=f"{settings.prefix}/docs", openapi_url=f"{settings.prefix}/openapi.json")
app.add_middleware(ClientIPLoggerMiddleware)
app.include_router(job_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, proxy_headers=True, log_config=log_config, forwarded_allow_ips='*')