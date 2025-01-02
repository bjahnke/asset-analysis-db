from invoke import task
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

@task
def ci_build(ctx):
    """
    Task to run the buildAll task for CI.
    """
    buildAll(ctx)

@task
def ci_test(ctx):
    """
    Task to run tests using pytest for CI.
    """
    ctx.run("python -m pytest")


@task
def start_ci_jupyter_env(ctx, clean=False):
    """
    Start a CI Jupyter environment.
    
    :param clean: If True, closes/deletes the existing act container if any exists (running or otherwise).
    """
    container_name = "act-ci-jupyter-env"
    image_name = "catthehacker/ubuntu:act-latest"

    if clean:
        # Stop and remove the existing container if it exists
        print("Stopping and removing existing container if it exists...")
        ctx.run(f"docker stop {container_name}", warn=True)
        ctx.run(f"docker rm {container_name}", warn=True)

    # Pull the latest image
    print("Pulling the latest image...")
    ctx.run(f"docker pull {image_name}")

    # Create the container
    print("Creating the container...")
    # Check if the container already exists
    result = ctx.run(f"docker ps -a --filter name={container_name} --format '{{{{.Names}}}}'", hide=True)
    if container_name not in result.stdout:
        ctx.run(f"docker create --name {container_name} {image_name}")
    else:
        print(f"Container {container_name} already exists.")

    # Start the container
    print("Starting the container...")
    print('docker start', container_name)
    ctx.run(f"docker start {container_name}")
    # Block until the container is ready
    print("Waiting for the container to be ready...")
    ctx.run(f"docker exec {container_name} bash -c 'until curl -s http://localhost:8888 > /dev/null; do sleep 1; done'")
    # Install Jupyter Notebook inside the container
    print("Installing Jupyter Notebook inside the container...")
    ctx.run(f"docker exec {container_name} apt-get update")
    ctx.run(f"docker exec {container_name} apt-get install -y python3-pip")
    ctx.run(f"docker exec {container_name} pip3 install notebook")

    # Start Jupyter Notebook server
    print("Starting Jupyter Notebook server inside the container...")
    ctx.run(f"docker exec -d {container_name} jupyter notebook --ip=0.0.0.0 --allow-root --no-browser")

    print("Jupyter Notebook server started. You can access it at http://localhost:8888")

@task
def stop_ci_jupyter_env(ctx):
    """
    Stop and remove the CI Jupyter environment container.
    """
    container_name = "act-ci-jupyter-env"
    print("Stopping the container...")
    ctx.run(f"docker stop {container_name}", warn=True)
    print("Removing the container...")
    ctx.run(f"docker rm {container_name}", warn=True)
    print("Container stopped and removed.")