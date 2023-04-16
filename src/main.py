from time import perf_counter
from typing import List

from absl import app
from absl.flags import FLAGS
from loguru import logger

from apollo.container import ApolloContainer
from apollo.map_service import load_map_service
from apollo.utils import change_apollo_map
from config import APOLLO_ROOT, PROJECT_NAME
from scenoRITA.components.scenario_generator import ScenarioGenerator
from scenoRITA.operators import GeneticOperators
from utils import generate_id, set_up_gflags, set_up_logging


def start_containers(num_adc: int) -> List[ApolloContainer]:
    containers = [
        ApolloContainer(APOLLO_ROOT, f"{PROJECT_NAME}_{generate_id()}")
        for _ in range(num_adc)
    ]
    for ctn in containers:
        if not FLAGS.dry_run:
            ctn.start_container()
            logger.info(f"{ctn.container_name} @ {ctn.container_ip()}")
    return containers


def main(argv):
    del argv
    set_up_logging(FLAGS.log_level)
    logger.info("Execution ID: " + FLAGS.execution_id)
    logger.info("Map: " + FLAGS.map)
    logger.info("Number of ADSes: " + str(FLAGS.num_adc))
    logger.info("Length of experiment: {}h", FLAGS.num_hour)

    # change map used by Apollo
    logger.info("Changing map to " + FLAGS.map)
    change_apollo_map(FLAGS.map)

    # start up Apollo containers
    logger.info("Starting up Apollo containers")
    containers = start_containers(FLAGS.num_adc)

    # loading map service
    logger.info(f"Loading map service for {FLAGS.map}")
    map_service = load_map_service(FLAGS.map)

    # genetic algorithm main loop
    scenario_generator = ScenarioGenerator(map_service)
    genetic_operators = GeneticOperators(
        map_service,
        FLAGS.mut_pb,
        FLAGS.cx_pb,
        FLAGS.add_pb,
        FLAGS.del_pb,
        FLAGS.replace_pb,
        FLAGS.min_obs,
        FLAGS.max_obs,
        FLAGS.dry_run,
    )

    ga_start_time = perf_counter()
    expected_end_time = ga_start_time + FLAGS.num_hour * 3600

    scenarios = [
        scenario_generator.generate_scenario(0, x, FLAGS.min_obs, FLAGS.max_obs)
        for x in range(FLAGS.num_scenario)
    ]
    genetic_operators.evaluate(containers, scenarios)

    generation_counter = 1
    while perf_counter() < expected_end_time:
        logger.info(f"Generation {generation_counter}")
        offsprings = genetic_operators.get_offsprings(scenarios)
        for sce in offsprings:
            logger.debug(
                f"Offspring {sce.get_id()} has {len(sce.obstacles)} obstacles."
            )
        genetic_operators.evaluate(containers, offsprings)
        scenarios = genetic_operators.select(scenarios, offsprings)
        generation_counter += 1

        if FLAGS.dry_run and generation_counter == 5:
            break


if __name__ == "__main__":
    set_up_gflags()
    app.run(main)
