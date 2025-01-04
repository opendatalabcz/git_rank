import uvicorn
from dependency_injector import containers, providers
from fastapi import FastAPI

from git_rank import CONFIG_PATH
from git_rank.logging import init_logging


class ApplicationContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.from_yaml(CONFIG_PATH)

    logging = providers.Resource(init_logging, config=config.logging)

    fast_api = providers.Factory(FastAPI)

    uvicorn_runner = providers.Callable(uvicorn.run)
