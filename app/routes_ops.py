from fastapi import APIRouter

router = APIRouter(tags=["ops"])


@router.get("/healthz")
def healthz():
    return {"status": "ok"}


@router.get("/version")
def version():
    return {"version": "1.0.0", "name": "user-api"}
