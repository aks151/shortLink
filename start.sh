#!/bin/bash

# This command starts Gunicorn, which acts as a process manager for Uvicorn workers.
# Gunicorn is responsible for starting multiple worker processes, monitoring them,
# and restarting them if they fail.
#
# -w 4: Spawns 4 worker processes. A good starting point is 2-4 workers per CPU core.
# -k uvicorn.workers.UvicornWorker: Tells Gunicorn to use Uvicorn to run the actual
#    ASGI application (FastAPI). This is the "magic glue".
# app.main:app: The location of your FastAPI app instance.
# --bind 0.0.0.0:8000: Binds the server to all network interfaces on port 8000,
#    which is necessary for it to be reachable within a container.
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
