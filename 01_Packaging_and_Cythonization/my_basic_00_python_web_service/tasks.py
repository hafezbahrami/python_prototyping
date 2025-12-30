"""
tasks.py

Simple development tasks for the basic Python web service.
"""

import os
from invoke import task, Context

APP_MODULE = "basic_service.app:app"
DEFAULT_PORT = 8000
ENV = os.getenv("ENV", "prod")


@task
def run(ctx: Context, port: int = DEFAULT_PORT) -> None:
    """
    Run the development server using uvicorn.

    Uses --reload automatically in dev mode.
    """

    reload_flag = "--reload" if ENV == "dev" else ""

    ctx.run(
        f"uvicorn {APP_MODULE} --host 127.0.0.1 --port {port} {reload_flag}",
        echo=True,
    )


@task
def format(ctx: Context) -> None:
    """
    Format code using black.
    """

    ctx.run("black .", echo=True)


@task
def lint(ctx: Context) -> None:
    """
    Run basic linting checks.
    """

    ctx.run("python -m pyflakes src", echo=True)


@task
def test(ctx: Context) -> None:
    """
    Run tests.
    """

    ctx.run("pytest -v", echo=True)


@task
def info(ctx: Context) -> None:
    """
    Print useful environment information.
    """

    print("Application module:", APP_MODULE)
    print("Environment:", ENV)
