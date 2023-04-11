from absl import app
from absl.flags import FLAGS
from loguru import logger

from apollo.utils import change_apollo_map
from utils import set_up_gflags, set_up_logging


def main(argv):
    del argv
    set_up_logging("INFO")
    logger.info("Execution ID: " + FLAGS.execution_id)
    logger.info("Map: " + FLAGS.map)
    logger.info("Number of ADSes: " + str(FLAGS.num_adc))
    logger.info("Length of experiment: {}h", FLAGS.num_hour)

    # change map used by Apollo
    logger.info("Changing map to " + FLAGS.map)
    change_apollo_map(FLAGS.map)

    # start up Apollo containers
    logger.info("Starting up Apollo containers")


if __name__ == "__main__":
    set_up_gflags()
    app.run(main)
