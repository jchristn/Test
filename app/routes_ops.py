import time

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.store import list_users

router = APIRouter(tags=["ops"])
PROCESS_START_TIME = time.monotonic()


@router.get("/healthz")
def healthz():
    return {"status": "ok", "name": "user-api"}


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
        "status": "ready",
        "uptime_seconds": time.monotonic() - PROCESS_START_TIME,
    }


@router.get("/version")
def version():
    return {"version": "1.0.0", "name": "user-api", "status": "stable"}
