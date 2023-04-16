import multiprocessing as mp
from pathlib import Path
from time import perf_counter
from typing import List

from absl import app
from absl.flags import FLAGS
from loguru import logger

from apollo.container import ApolloContainer
from apollo.map_service import load_map_service
from apollo.utils import change_apollo_map
from config import APOLLO_ROOT, PROJECT_NAME
from mylib.workers import analysis_worker, generator_worker, player_worker
from scenoRITA.components.grading_metrics import GradingResult
from scenoRITA.components.scenario_generator import ScenarioGenerator
from scenoRITA.operators import GeneticOperators
from scenoRITA.representation import Scenario
from utils import generate_id, get_output_dir, set_up_gflags, set_up_logging


def evaluate_scenarios(containers: List[ApolloContainer], scenarios: List[Scenario]):
    num_workers = 5
    with mp.Manager() as manager:
        # set up queues
        pending_queue = manager.Queue()
        play_queue = manager.Queue()
        analysis_queue = manager.Queue()
        result_queue: "mp.Queue[GradingResult]" = manager.Queue()  # type: ignore
        for scenario in scenarios:
            pending_queue.put(scenario)
        for _ in range(num_workers):
            pending_queue.put(None)

        # set up processes
        generator_processes = [
            mp.Process(
                target=generator_worker,
                args=(
                    ScenarioGenerator(load_map_service(FLAGS.map)),
                    logger,
                    pending_queue,
                    play_queue,
                    get_output_dir(),
                    FLAGS.dry_run,
                ),
            )
            for _ in range(num_workers)
        ]
        player_processes = [
            mp.Process(
                target=player_worker,
                args=(
                    containers[x],
                    load_map_service(FLAGS.map),
                    logger,
                    play_queue,
                    analysis_queue,
                    get_output_dir(Path(f"/{PROJECT_NAME}"), False),
                    FLAGS.dry_run,
                ),
            )
            for x in range(len(containers))
        ]
        analyzer_processes = [
            mp.Process(
                target=analysis_worker,
                args=(
                    load_map_service(FLAGS.map),
                    logger,
                    analysis_queue,
                    result_queue,
                    get_output_dir(),
                    FLAGS.dry_run,
                ),
            )
            for _ in range(num_workers)
        ]

        # start processes
        for p in generator_processes:
            p.start()
        for p in player_processes:
            p.start()
        for p in analyzer_processes:
            p.start()

        # wait for processes to finish
        for p in generator_processes:
            p.join()
        for _ in range(len(player_processes)):
            play_queue.put(None)
        for p in player_processes:
            p.join()
        for _ in range(len(analyzer_processes)):
            analysis_queue.put(None)
        for p in analyzer_processes:
            p.join()

        # TODO: update scenario with result_queue


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
    evaluate_scenarios(containers, scenarios)

    generation_counter = 1
    while perf_counter() < expected_end_time:
        logger.info(f"Generation {generation_counter}: start")
        offsprings = genetic_operators.get_offsprings(scenarios)
        logger.info(f"Generation {generation_counter}: mut/cx done")
        evaluate_scenarios(containers, offsprings)
        logger.info(f"Generation {generation_counter}: evaluation done")
        scenarios = genetic_operators.select(scenarios, offsprings)
        logger.info(f"Generation {generation_counter}: selection done")
        logger.info(f"Generation {generation_counter}: end")

        generation_counter += 1
        if FLAGS.dry_run and generation_counter == 5:
            break


if __name__ == "__main__":
    set_up_gflags()
    app.run(main)
