from fastapi import FastAPI, HTTPException, Request
from kubernetes import client, config
from pydantic import BaseModel

app = FastAPI(docs_url="/docs")

# Load the Kubernetes configuration
# Use this for local development
# config.load_kube_config()

# Use this when running in a pod within the cluster
config.load_incluster_config()

NAMESPACE = "your-namespace"

class JobSpec(BaseModel):
    name: str
    repo_url: str

def create_job(job_spec: JobSpec):
    job = client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=client.V1ObjectMeta(name=job_spec.name),
        spec=client.V1JobSpec(
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels={"job": job_spec.name}),
                spec=client.V1PodSpec(
                    containers=[
                        client.V1Container(
                            name="alpine-container",
                            image="alpine:latest",
                            command=["/bin/sh", "-c", "echo $REPO_URL"],
                            env=[client.V1EnvVar(name="REPO_URL", value=job_spec.repo_url)]
                        )
                    ],
                    restart_policy="Never"
                )
            )
        )
    )

    batch_v1 = client.BatchV1Api()
    batch_v1.create_namespaced_job(namespace=NAMESPACE, body=job)

@app.post("/webhook")
async def trigger_job(request: Request):
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)