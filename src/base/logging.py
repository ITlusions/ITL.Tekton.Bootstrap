import sys
import logging.config
from uvicorn.logging import AccessFormatter

access_log_format = '%(asctime)s :: %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'

def get_log_config():
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'},
            'access': {'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'},
        },
        'handlers': {
            'default': {'formatter': 'default', 'class': 'logging.StreamHandler', 'stream': sys.stderr},
            'access': {'formatter': 'access', 'class': 'logging.StreamHandler', 'stream': sys.stdout},
        },
        'loggers': {
            'uvicorn.error': {'level': 'INFO', 'handlers': ['default'], 'propagate': False},
            'uvicorn.access': {'level': 'INFO', 'handlers': ['access'], 'propagate': False},
        },
        'root': {'level': 'DEBUG', 'handlers': ['default'], 'propagate': False},
    }

# Apply logging configuration directly here
def setup_logging():
    logging.config.dictConfig(get_log_config())