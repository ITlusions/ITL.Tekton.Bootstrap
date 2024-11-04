from fastapi import FastAPI, HTTPException, Request
import subprocess
import os

app = FastAPI(docs_url="/docs")

# Kubernetes namespace where the CronJob is located
NAMESPACE = "your-namespace"  # Replace with your actual namespace

@app.post("/webhook")
async def trigger_job(request: Request):
    # Get the headers and payload from the request
    event_type = request.headers.get("X-GitHub-Event")
    if event_type != "repository":
        raise HTTPException(status_code=400, detail="Invalid event type")

    payload = await request.json()

    # Check if the repository is created
    if payload.get("action") == "created":
        try:
            job_name = "tkn-bootstrap-repo-job"  # The name for the new Job

            # Command to create the Job from the CronJob
            command = [
                "kubectl",
                "create",
                "job",
                "--from=cronjob/pac-bootstrap-cronjob",
                job_name,
                "-n",
                NAMESPACE
            ]

            # Execute the command
            result = subprocess.run(command, check=True, capture_output=True, text=True)

            return {"message": "Job created successfully", "output": result.stdout}

        except subprocess.CalledProcessError as e:
            raise HTTPException(status_code=500, detail=f"Error creating job: {e.stderr}")

    return {"message": "No action taken, not a repository creation event."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
