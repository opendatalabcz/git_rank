#!/bin/bash
set -e

exec uvicorn git_rank.__main__:app --factory --host ${SERVER_HOST} --port ${SERVER_PORT}
