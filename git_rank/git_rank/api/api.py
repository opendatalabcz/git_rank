from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from structlog import get_logger

from git_rank.application.ranking_orchestrator import RankingOrchestrator
from git_rank.containers.ranking_orchestrator_container import RankingOrchestratorContainer
from git_rank.models.statistics.user_statistics import UserStatistics

router = APIRouter()

logger = get_logger()


@router.get("/rank/{username}")
@inject
def rank_user(
    username: str,
    ranking_orchestrator: RankingOrchestrator = Depends(
        Provide[RankingOrchestratorContainer.ranking_orchestrator]
    ),
) -> UserStatistics:

    return ranking_orchestrator.rank_user(username)


@router.get("/status")
def get_status() -> dict[str, str]:
    logger.info("get_status")
    return {"status": "OK"}
