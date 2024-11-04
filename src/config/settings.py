from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    prefix: str = '/tkn'
    jobs_namespace: str = 'tkn-bootstrap'

    class Config:
        env_file = '.env'

settings = Settings()