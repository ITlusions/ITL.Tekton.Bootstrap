from fastapi import FastAPI
from routers.job_router import router as job_router
from config.settings import settings
import sys

app = FastAPI(docs_url=f"{settings.prefix}/docs", openapi_url=f"{settings.prefix}/openapi.json")

app.include_router(job_router)

if __name__ == "__main__":
    import uvicorn
    log_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            },
            'access': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            },
        },
        'handlers': {
            'default': {
                'formatter': 'default',
                'class': 'logging.StreamHandler',
                'stream': sys.stderr,
            },
            'access': {
                'formatter': 'access',
                'class': 'logging.StreamHandler',
                'stream': sys.stdout,
            },
        },
        'loggers': {
            'uvicorn.error': {
                'level': 'INFO',
                'handlers': ['default'],
                'propagate': False,
            },
            'uvicorn.access': {
                'level': 'INFO',
                'handlers': ['access'],
                'propagate': False,
            },
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['default'],
            'propagate': False,
        },
    }
    uvicorn.run(app, host="0.0.0.0", port=8000, proxy_headers=True, log_config=log_config, forwarded_allow_ips='*')