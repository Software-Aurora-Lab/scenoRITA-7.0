import os
import string
import sys
from datetime import datetime
from pathlib import Path

from absl import flags
from absl.flags import FLAGS
from loguru import logger
from nanoid import generate

from config import LOGGING_FORMAT, OUT_DIR, PROJECT_NAME


def generate_id(size=5):
    return generate(string.ascii_letters, size=size)


def set_up_gflags():
    # Execution flags
    flags.DEFINE_string("map", "borregas_ave", "Name of the map to use.")
    flags.DEFINE_integer("num_adc", 1, "Number of ADCs to use.")
    flags.DEFINE_boolean("dry_run", os.uname()[0] != "Linux", "Dry run mode.")
    flags.DEFINE_string(
        "execution_id", datetime.now().strftime("%y%m%d_%H%M%S"), "Execution ID."
    )
    flags.DEFINE_boolean("colorize", True, "Colorize log output.")

    # Genetic algorithm flags
    flags.DEFINE_integer("num_scenario", 50, "Number of scenarios to generate.")
    flags.DEFINE_integer("num_hour", 12, "Number of hours to generate scenarios for.")
    flags.DEFINE_integer("min_obs", 3, "Minimum number of obstacles.")
    flags.DEFINE_integer("max_obs", 10, "Maximum number of obstacles.")


def get_output_dir() -> Path:
    result = Path(OUT_DIR, f"{FLAGS.execution_id}_{FLAGS.map}")
    if not result.exists():
        result.mkdir(parents=True)
    return result


def get_log_file() -> Path:
    return Path(OUT_DIR, f"{FLAGS.execution_id}_{FLAGS.map}", f"{PROJECT_NAME}.log")


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
