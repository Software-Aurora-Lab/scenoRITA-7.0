# scenoRITA for Baidu Apollo v7.0.0

<a href="https://zenodo.org/10.5281/zenodo.8231346">
   <img src="https://img.shields.io/badge/DOI-10.5281%2Fzenodo.8231345-blue?style=flat-square&logo=doi"/>
</a>

This is an implementation of scenoRITA that supports Baidu Apollo v7.0.0. Please find the most up-to-date version with updates and fixes at our [GitHub repository](https://github.com/Software-Aurora-Lab/scenoRITA-7.0/).

## Prerequisites

1. Ubuntu 20.04 LTS
2. [Docker CE](https://docs.docker.com/engine/install/ubuntu/)
3. [Python Poetry](https://python-poetry.org/)
4. [Python 3.11](https://www.python.org/downloads/release/python-3110/)

> You can run scripts under `data/scripts/install` to install the prerequisites.

## Running scenoRITA

0. Install prerequisites needed using scripts under `data/scripts/install`.

1. Install project dependencies via command
   ```
   poetry install
   ```

2. Install Apollo v7.0.0 via command
   ```
   poetry run python src/install.py
   ```
   this command will download a release version of Apollo v7.0.0 and compile necessary modules.

3. Run scenoRITA via command
   ```
   poetry run python src/main.py
   ```
   
   > if you want to run scenoRITA on different maps (e.g., san_mateo), you can add `--map=san_mateo` to command.

4. To reproduce experiments described in the paper (e.g., running scenoRITA on San Francisco), run
   ```
   source run_experiments.sh
   san_francisco
   ```

After running the command, the output of scenoRITA will be stored under `out/{execution_id}` and you can find violations detected under `out/{execution_id}/violations`
