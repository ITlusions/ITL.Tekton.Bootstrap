from kubernetes import client, config
from models.job_model import JobSpec
from config.settings import settings 

# Load the Kubernetes configuration
config.load_incluster_config()

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
    batch_v1.create_namespaced_job(namespace=settings.jobs_namespace, body=job)
