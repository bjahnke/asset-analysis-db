from invoke import task
from src.util_invoke_tasks import *
import os

@task
def build(ctx):
    """
    Build the Docker image without using the cache and log the output to build.log.
    """
    print("Starting Docker image build...")
    result = ctx.run("docker-compose -f ./docker/docker-compose.yml build --no-cache", warn=True)
    with open("build.log", "w") as f:
        f.write(result.stdout)
    if result.ok:
        print("Docker image built successfully.")
    else:
        print("Failed to build Docker image. Check build.log for details.")

@task
def start(ctx):
    """
    Stop any running Docker containers, start the Docker container, and log the output to run.log.
    """
    ctx.run("docker-compose -f docker/docker-compose.yml down -v")
    result = ctx.run("docker-compose -f docker/docker-compose.yml up -d --force-recreate", warn=True)
    with open("run.log", "w") as f:
        f.write(result.stdout)
    if result.ok:
        print("Docker container started successfully.")
    else:
        print("Failed to start Docker container. Check run.log for details.")

@task
def generate_orm(ctx):
    """
    Generate ORM models from the PostgreSQL database and save them to model.py.
    """
    ctx.run("sqlacodegen postgresql+psycopg2://postgres:password@0.0.0.0/asset_analysis > ./asset_db/model.py")

@task
def stop(ctx):
    """
    Stop the Docker container and remove volumes.
    """
    ctx.run("docker-compose -f ./docker/docker-compose.yml down -v")

@task
def buildAll(ctx):
    """
    Build the Docker image, run the container, generate ORM models, and stop the container.
    """
    build(ctx)
    start(ctx)
    # container is run in detached mode, so wait a moment for it to start up
    ctx.run("sleep 1")
    generate_orm(ctx)
    stop(ctx)