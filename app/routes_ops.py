import time

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.store import list_users

router = APIRouter(tags=["ops"])
PROCESS_START_TIME = time.monotonic()
SERVICE_NAME = "user-api"
SERVICE_VERSION = "1.0.0"


def _service_metadata(status: str):
    return {"status": status, "name": SERVICE_NAME, "version": SERVICE_VERSION}


@router.get("/healthz")
def healthz():
    return _service_metadata("ok")


@router.get("/readyz")
def readyz():
    try:
        list_users()
    except Exception as exc:
        return JSONResponse(
            status_code=503,
            content={"status": "not_ready", "reason": str(exc)},
        )
    return {
        **_service_metadata("ready"),
        "uptime_seconds": time.monotonic() - PROCESS_START_TIME,
    }


@router.get("/version")
def version():
    return {
        "version": SERVICE_VERSION,
        "name": SERVICE_NAME,
        "status": "stable",
        "runtime": "fastapi",
    }
