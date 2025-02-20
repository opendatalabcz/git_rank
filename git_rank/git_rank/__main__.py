import typer
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from structlog import get_logger

from git_rank.api import api
from git_rank.containers.application_container import ApplicationContainer

logger = get_logger()
cli = typer.Typer(name="git_rank", add_completion=False)


def create_application_container() -> ApplicationContainer:
    application_container = ApplicationContainer()
    application_container.init_resources()
    return application_container


def create_application(application_container: ApplicationContainer) -> FastAPI:
    fast_api = application_container.fast_api()
    fast_api.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:8091"],
        allow_credentials=True,
        allow_methods=["GET"],
        allow_headers=["*"],
    )
    fast_api.include_router(api.router)
    return fast_api


@cli.command()
def app() -> FastAPI:
    application_container = create_application_container()
    return create_application(application_container)


@cli.command()
def server() -> None:
    application_container = create_application_container()
    fast_api = create_application(application_container)

    config = application_container.config()
    host = config["server"]["host"]
    port = config["server"]["port"]

    logger.debug("server.start", host=host, port=port)
    application_container.uvicorn_runner(fast_api, host=host, port=port)


if __name__ == "__main__":
    cli()
