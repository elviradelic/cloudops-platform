import os
import platform
import socket
import time

from fastapi import FastAPI
from app.config import APP_ENV
from app.database import check_database_connection


app = FastAPI(
    title="CloudOps Status API",
    description="Backend service for the CloudOps DevOps portfolio platform.",
    version="1.0.0",
)

START_TIME = time.time()


@app.get("/")
def root():
    return {
        "message": "CloudOps Status API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/api/status")
def status():
    uptime_seconds = int(time.time() - START_TIME)

    return {
        "status": "healthy",
        "service": "cloudops-backend",
        "version": "1.0.0",
        "environment": APP_ENV,
        "hostname": socket.gethostname(),
        "platform": platform.system(),
        "uptime_seconds": uptime_seconds,
    }

@app.get("/api/database")
def database_status():
    return check_database_connection()