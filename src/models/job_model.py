from pydantic import BaseModel

class JobSpec(BaseModel):
    name: str
    repo_url: str
