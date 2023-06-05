import os
import string
import sys
from datetime import datetime
from pathlib import Path

from absl import flags
from absl.flags import FLAGS
from loguru import logger
from nanoid import generate

from config import LOGGING_FORMAT, PROJECT_NAME, PROJECT_ROOT


def generate_id(size=5):
    return generate(string.ascii_letters, size=size)


def set_up_gflags():
    # Execution flags
    flags.DEFINE_string("map", "borregas_ave", "Name of the map to use.")
    flags.DEFINE_integer("num_adc", 5, "Number of ADCs to use.")
    flags.DEFINE_boolean("dry_run", os.uname()[0] != "Linux", "Dry run mode.")
    flags.DEFINE_boolean("dreamview", False, "Enable Dreamview.")
    flags.DEFINE_string(
        "execution_id", datetime.now().strftime(r"%m%d_%H%M%S"), "Execution ID."
    )
    flags.DEFINE_integer("perception_frequency", 10, "Perception frequency.")
    flags.DEFINE_integer("scenario_length", 30, "Length of the scenario in seconds.")
    flags.DEFINE_boolean("colorize", True, "Colorize log output.")
    flags.DEFINE_string("log_level", "INFO", "Log level.")

    # Genetic algorithm flags
    flags.DEFINE_integer("num_scenario", 20, "Number of scenarios to generate.")
    flags.DEFINE_float("num_hour", 12.0, "Number of hours to generate scenarios for.")
    flags.DEFINE_integer("min_obs", 5, "Minimum number of obstacles.")
    flags.DEFINE_integer("max_obs", 15, "Maximum number of obstacles.")

    flags.DEFINE_float("mut_pb", 0.2, "Probability of mutation.")
    flags.DEFINE_float("cx_pb", 0.8, "Probability of crossover.")
    flags.DEFINE_float("add_pb", 0.1, "Probability of adding an obstacle.")
    flags.DEFINE_float("del_pb", 0.1, "Probability of deleting an obstacle.")
    flags.DEFINE_float("replace_pb", 0.1, "Probability of replacing the ego car.")


def get_output_dir(root: Path = PROJECT_ROOT, mkdir: bool = True) -> Path:
    result = Path(root, "out", f"{FLAGS.execution_id}_{FLAGS.map}")
    if not result.exists() and mkdir:
        result.mkdir(parents=True)
    return result


def get_log_file() -> Path:
    return Path(
        PROJECT_ROOT, "out", f"{FLAGS.execution_id}_{FLAGS.map}", f"{PROJECT_NAME}.log"
    )


def set_up_logging(level: str | int) -> None:
    # set up logging
    logger.remove()
    logger.add(get_log_file(), format=LOGGING_FORMAT, level=level, enqueue=True)
    logger.add(
        sys.stdout,
        format=LOGGING_FORMAT,
        colorize=FLAGS.colorize,
        level=level,
        enqueue=True,
    )
