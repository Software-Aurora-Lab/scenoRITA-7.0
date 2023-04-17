# scenoRITA for Apollo v7.0.0

## Prerequisites

1. Ubuntu 20.04 LTS
2. [Docker CE](https://docs.docker.com/engine/install/ubuntu/)
3. [Python Poetry](https://python-poetry.org/)
4. [Python 3.11](https://www.python.org/downloads/release/python-3110/)

> You can run scripts under `data/scripts/install` to install the prerequisites.

## Running scenoRITA

1. Install Apollo v7.0.0 via command
   ```
   poetry run python src/install.py
   ```
   this command will download a release version of Apollo v7.0.0 and compile necessary modules.

2. Run scenoRITA via command
   ```
   poetry run python src/main.py
   ```
   
   > if you want to run scenoRITA on different maps (e.g., san_mateo), you can add `--map=san_mateo` to command.

After running the command, the output of scenoRITA will be stored under `out/{execution_id}` and you can find violations detected under `out/{execution_id}/violations`
