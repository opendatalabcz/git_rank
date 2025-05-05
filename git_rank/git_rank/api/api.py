from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException
from pydantic import HttpUrl
from structlog import get_logger

from git_rank.application.ranking_orchestrator import RankingOrchestrator
from git_rank.containers.ranking_orchestrator_container import RankingOrchestratorContainer
from git_rank.exceptions.ranking_exceptions import RankingAlreadyRunningException
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
    try:
        return ranking_orchestrator.rank_user(username)
    except RankingAlreadyRunningException as e:
        raise HTTPException(
            status_code=409,
            detail=f"Ranking already running for user {username}. Please try again later.",
        ) from e


@router.get("/rank/{username}/repository")
@inject
def rank_repository(
    username: str,
    repository_url: HttpUrl,
    ranking_orchestrator: RankingOrchestrator = Depends(
        Provide[RankingOrchestratorContainer.ranking_orchestrator]
    ),
) -> UserStatistics:
    try:
        return ranking_orchestrator.rank_user_repository(
            username=username, repository_url=str(repository_url)
        )
    except RankingAlreadyRunningException as e:
        raise HTTPException(
            status_code=409,
            detail=f"Ranking already running for user {username} and repository {repository_url}. Please try again later.",
        ) from e


@router.get("/status")
def get_status() -> dict[str, str]:
    logger.info("get_status")
    return {"status": "OK"}
