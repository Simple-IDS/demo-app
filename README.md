# Demo App
Simple Flask app with /login and /search endpoints.

## Run locally with Docker

Build the image and run it (binds to host port 8000 by default):

```bash
docker build -t simple-ids-demo .
docker run -p 8000:8000 simple-ids-demo
```

The app listens on 0.0.0.0:$PORT inside the container. You can set a different port with `-e PORT=xxxx`.

## Deploy to a container host or PaaS

This app can be deployed to any Docker-friendly host (Render, Fly.io, DigitalOcean App Platform, Heroku-like services).

- Ensure the platform exposes the container PORT environment variable (default 8000).
- We include a `Procfile` for platforms that use it; the container entrypoint uses `gunicorn`.

Example quick notes:

- Render: create a Web Service, link the repo, and set the Dockerfile build; the service will use the exposed PORT.
- Fly.io: `fly launch` and `fly deploy` will detect the Dockerfile and deploy the container.
- DigitalOcean App Platform: choose 'Dockerfile' when creating a component and set the port to 8000.

