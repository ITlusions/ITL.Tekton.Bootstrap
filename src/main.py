from fastapi import FastAPI
from routers.job_router import router as job_router
from routers.test_router import router as test_router
from config.settings import settings
from base.logging import setup_logging
from middleware.log_client_ip import ClientIPLoggerMiddleware

log_config = setup_logging()

app = FastAPI(docs_url="/docs", root_path="/tkn")

appv1 = FastAPI(docs_url=f"/docs", openapi_url=f"/openapi.json")
appv2 = FastAPI(docs_url=f"/docs", openapi_url=f"/openapi.json")

app.mount(f"{settings.prefix}/v1", appv1)
app.mount(f"{settings.prefix}/v2", appv2)

appv1.add_middleware(ClientIPLoggerMiddleware)
appv2.add_middleware(ClientIPLoggerMiddleware)
appv1.include_router(job_router)
appv2.include_router(test_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, proxy_headers=True, log_config=log_config, forwarded_allow_ips='*')