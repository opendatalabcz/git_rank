from fastapi import APIRouter
from structlog import get_logger

router = APIRouter()

logger = get_logger()


@router.get("/status")
def get_status() -> dict[str, str]:
    logger.info("get_status")
    return {"status": "OK"}
