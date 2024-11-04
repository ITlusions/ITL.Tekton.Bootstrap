# Use an official Python runtime based on Alpine as a parent image
FROM ghcr.io/astral-sh/uv:python3.12-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY /src .
COPY requirements.txt /tmp/requirements.txt
# Install dependencies including uv
RUN apk add --no-cache curl gcc musl-dev linux-headers
RUN curl -lsSf https://bootstrap.pypa.io/get-pip.py | python
RUN pip install -r /tmp/requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# Command to run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]