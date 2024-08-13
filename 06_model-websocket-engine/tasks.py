from multiprocessing import Process

from invoke import task


@task
def validate(ctx):
    """validate"""
    ctx.run("black --check --diff  --verbose .", echo=True)
    ctx.run("mypy --install-types --non-interactive .", echo=True)


@task
def fmt(ctx):
    ctx.run("black .")


@task
def ui(ctx):
    ctx.run(
        "python -m http.server --bind 0.0.0.0 --directory ./user_interface/ 8000",
        echo=True,
        pty=True,
    )


@task
def eng(ctx):
    ctx.run("python ./evaluation_server/main.py", echo=True, pty=True)


@task
def run(ctx):
    # Start ui server
    pass
