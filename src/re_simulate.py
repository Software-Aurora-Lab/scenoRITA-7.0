import multiprocessing as mp
import shutil
import threading
from pathlib import Path
from time import perf_counter
import time
from typing import Dict, List

from absl import app
from absl.flags import FLAGS
from loguru import logger

from apollo.container import ApolloContainer
from apollo.map_service import load_map_service
from apollo.utils import change_apollo_map, clean_apollo_logs
from config import APOLLO_ROOT, PROJECT_NAME, PROJECT_ROOT
from mylib.clustering import cluster
from mylib.workers import analysis_worker, generator_worker, player_worker
from scenoRITA.components.grading_metrics import GradingResult
from scenoRITA.components.scenario_generator import ScenarioGenerator
from scenoRITA.operators import GeneticOperators
from scenoRITA.representation import Scenario
from utils import generate_id, get_output_dir, set_up_gflags, set_up_logging
from cyber_record.record import Record

def load_routing_request(path: str):
    r = Record(path)
    for topic, msg, t in r.read_messages("/apollo/routing_request"):
        x, y, h = msg.waypoint[0].pose.x, msg.waypoint[0].pose.y, msg.waypoint[0].heading
        return (x, y), h


def start_containers(num_adc: int) -> List[ApolloContainer]:
    containers = [
        ApolloContainer(APOLLO_ROOT, f"{PROJECT_NAME}_{generate_id()}")
        for _ in range(num_adc)
    ]
    for ctn in containers:
        if not FLAGS.dry_run:
            ctn.start_container()
            if FLAGS.dreamview:
                ctn.start_dreamview()
            logger.info(f"{ctn.container_name} @ {ctn.container_ip()}")
    return containers


def main(argv):
    del argv
    set_up_logging(FLAGS.log_level)
    logger.info("Execution ID: " + FLAGS.execution_id)
    logger.info("Map: " + FLAGS.map)
    logger.info("Number of ADSes: " + str(1))
    logger.info("Scenario per Generation: " + str(FLAGS.num_scenario))
    logger.info("Length of experiment: {}h", FLAGS.num_hour)
    logger.info("Obstacle Range: {} - {}", FLAGS.min_obs, FLAGS.max_obs)

    # change map used by Apollo
    logger.info("Changing map to " + FLAGS.map)
    change_apollo_map(FLAGS.map)

    # start up Apollo containers
    logger.info("Starting up Apollo containers")
    containers = start_containers(1)
    container = containers[0]
    container.start_dreamview()

    # loading map service
    logger.info(f"Loading map service for {FLAGS.map}")
    logger.info("Map service loaded")

    target_input_dir = Path(str(PROJECT_ROOT) + "/out/0318_220007_borregas_ave/input")
    target_output_dir = get_output_dir()
    Path(target_output_dir, "records").mkdir(parents=True, exist_ok=True)

    target_docker_input_dir = f"/{PROJECT_NAME}/out/0318_220007_borregas_ave/input"
    target_docker_output_dir = get_output_dir(Path(f"/{PROJECT_NAME}"), False)

    all_files = list(target_input_dir.iterdir())
    count = len(all_files)
    for i, file in enumerate(all_files):
        logger.info(f"Processing {i+1}/{count} {file.name}")
        sce_id = file.name
        record_path = Path(target_input_dir, sce_id)
        (x, y), h = load_routing_request(str(record_path))
        in_docker_path = Path(target_docker_input_dir, f"{sce_id}")
        in_docker_output = Path(target_docker_output_dir, "records", f"{sce_id}")
        container.stop_ads_modules()
        container.stop_sim_control()
        container.start_sim_control(x, y, h)
        container.start_ads_modules()
        container.start_recorder(str(in_docker_output))
        container.start_replay(str(in_docker_path))
        time.sleep(31)
        container.stop_recorder()
        container.stop_replay()
        container.stop_ads_modules()
        container.stop_sim_control()


if __name__ == "__main__":
    set_up_gflags()
    try:
        app.run(main)
    except Exception as e:
        logger.exception(e)
        raise e
