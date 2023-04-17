import multiprocessing as mp
import random
import time
from logging import Logger
from pathlib import Path
from typing import Optional

from apollo.container import ApolloContainer
from apollo.map_service import MapService
from scenoRITA.components.grading_metrics import GradingResult
from scenoRITA.components.scenario_generator import ScenarioGenerator
from scenoRITA.representation import ObstacleFitness, Scenario


def generator_worker(
    generator: ScenarioGenerator,
    _logger: Logger,
    scenario_length: int,
    perception_frequency: int,
    task_queue: "mp.Queue[Optional[Scenario]]",
    result_queue: mp.Queue,
    target_dir: Path,
):
    while True:
        scenario = task_queue.get()
        if scenario is None:
            break
        _logger.info(f"{scenario.get_id()}: generate start")

        target_file = Path(target_dir, "input", f"{scenario.get_id()}")
        target_file.parent.mkdir(parents=True, exist_ok=True)
        generator.write_scenario_to_file(
            scenario, target_file, scenario_length, perception_frequency
        )

        _logger.info(f"{scenario.get_id()}: generate end")
        result_queue.put(scenario)


def player_worker(
    container: ApolloContainer,
    map_service: MapService,
    _logger: Logger,
    scenario_length: int,
    task_queue: "mp.Queue[Optional[Scenario]]",
    result_queue: "mp.Queue[Optional[Scenario]]",
    target_dir: Path,
    target_docker_dir: Path,
    dry_run: bool,
):
    while True:
        scenario = task_queue.get()
        if scenario is None:
            break
        sce_id = scenario.get_id()
        _logger.info(f"{sce_id}: play start ({container.container_name})")

        target_output_path = Path(target_dir, "records", f"{sce_id}.00000")
        target_output_path.parent.mkdir(parents=True, exist_ok=True)
        if dry_run:
            with open(target_output_path, "w") as fp:
                fp.write("dry run")
        else:
            in_docker_path = Path(target_docker_dir, "input", f"{sce_id}")
            in_docker_output = Path(target_docker_dir, "records", f"{sce_id}")
            container.stop_ads_modules()
            container.stop_sim_control()
            ego_initial = scenario.ego_car.initial_position
            ep, et = map_service.get_lane_coord_and_heading(
                ego_initial.lane_id, ego_initial.s
            )
            container.start_sim_control(ep.x, ep.y, et)
            container.start_ads_modules()
            container.start_recorder(str(in_docker_output))
            container.start_replay(str(in_docker_path))
            time.sleep(scenario_length)
            container.stop_recorder()
            container.stop_replay()
            container.stop_ads_modules()
            container.stop_sim_control()

        _logger.info(f"{sce_id}: play end")
        result_queue.put(scenario)


def analysis_worker(
    map_service: MapService,
    _logger: Logger,
    task_queue: "mp.Queue[Optional[Scenario]]",
    result_queue: "mp.Queue[GradingResult]",
    target_dir: Path,
    dry_run: bool,
):
    while True:
        scenario = task_queue.get()
        if scenario is None:
            break
        sce_id = scenario.get_id()
        _logger.info(f"{sce_id}: analysis start")

        target_input_file = Path(target_dir, "records", f"{sce_id}.00000")
        assert target_input_file.exists()
        if dry_run:
            obs_ids = [obs.id for obs in scenario.obstacles]
            fitnesses = dict()
            for oid in obs_ids:
                fitnesses[oid] = tuple(
                    random.random() for _ in range(len(ObstacleFitness.weights))
                )
            result_queue.put(
                GradingResult(
                    scenario.get_id(),
                    fitnesses,
                    [],
                )
            )

        _logger.info(f"{sce_id}: analysis end")
