from fastapi import FastAPI
from routers.job_router import router as job_router
from config.settings import settings

app = FastAPI(docs_url=f"{settings.prefix}/docs", openapi_url=f"{settings.prefix}/openapi.json")

app.include_router(job_router)

if __name__ == "__main__":
    import uvicorn
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(asctime)s - %(levelname)s - %(message)s - Client IP: %(remote_addr)s",
            },
            "access": {
                "()": "uvicorn.logging.AccessFormatter",
                "fmt": '%(asctime)s::%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',
            },
        },
        "handlers": {
            "default": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            }
        },
        "root": {
            "handlers": ["default"],
            "level": "INFO",
        },
    }
    uvicorn.run(app, host="0.0.0.0", port=8000, proxy_headers=True, log_config=log_config)
