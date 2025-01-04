import os
from importlib import metadata as importlib_metadata

PACKAGE_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.join(PACKAGE_DIR, "..")
CONFIG_NAME = "config.yml"
CONFIG_PATH = os.path.join(ROOT_DIR, "config", CONFIG_NAME)


def get_version() -> str:
    try:
        return importlib_metadata.version(__name__)
    except importlib_metadata.PackageNotFoundError:  # pragma: no cover
        return "unknown"


version: str = get_version()
