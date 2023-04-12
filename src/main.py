from time import perf_counter

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
    containers = [
        ApolloContainer(APOLLO_ROOT, f"{PROJECT_NAME}_{generate_id()}")
        for _ in range(FLAGS.num_adc)
    ]
    for ctn in containers:
        logger.info(f"Starting container {ctn.container_name}")
        if not FLAGS.dry_run:
            ctn.start_container()
            ctn.start_dreamview()

    # loading map service
    logger.info(f"Loading map service for {FLAGS.map}")
    map_service = load_map_service(FLAGS.map)

    # genetic algorithm main loop
    scenario_generator = ScenarioGenerator(map_service)
    genetic_operators = GeneticOperators(map_service)

    ga_start_time = perf_counter()
    expected_end_time = ga_start_time + FLAGS.num_hour * 3600
    scenarios = [scenario_generator.generate_scenario(FLAGS.min_obs, FLAGS.max_obs)]
    genetic_operators.evaluate_scenarios(scenarios)

    generation_counter = 1
    while perf_counter() < expected_end_time:
        logger.info(f"Generation {generation_counter}")
        offsprings = genetic_operators.get_offsprings(scenarios)
        genetic_operators.evaluate_scenarios(offsprings)
        generation_counter += 1

        if FLAGS.dry_run:
            break


if __name__ == "__main__":
    set_up_gflags()
    app.run(main)
