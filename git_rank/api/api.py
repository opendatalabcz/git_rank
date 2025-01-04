from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from structlog import get_logger

from git_rank.application.ranking_orchestrator import RankingOrchestrator
from git_rank.containers.ranking_orchestrator_container import (
    RankingOrchestratorContainer,
)

router = APIRouter()

logger = get_logger()


@router.get("/rank/{username}")
@inject
def rank_user(
    username: str,
    ranking_orchestrator: RankingOrchestrator = Depends(
        Provide[RankingOrchestratorContainer.ranking_orchestrator]
    ),
) -> None:
    log = logger.bind(username=username)
    log.info("rank_user.start")

    ranking_orchestrator.rank_user(username)

    log.info("rank_user.end")


@router.get("/status")
def get_status() -> dict[str, str]:
    logger.info("get_status")
    return {"status": "OK"}
