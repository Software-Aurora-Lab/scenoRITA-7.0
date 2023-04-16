import multiprocessing as mp
from logging import Logger
from pathlib import Path
from typing import Optional

from apollo.container import ApolloContainer
from apollo.map_service import MapService
from scenoRITA.components.scenario_generator import ScenarioGenerator
from scenoRITA.representation import Scenario


def generator_worker(
    generator: ScenarioGenerator,
    _logger: Logger,
    task_queue: "mp.Queue[Optional[Scenario]]",
    result_queue: mp.Queue,
    target_dir: Path,
    dry_run: bool,
):
    while True:
        scenario = task_queue.get()
        if scenario is None:
            break
        _logger.info(f"{scenario.get_id()}: generate start")
        # TODO: generate scenario
        target_file = Path(target_dir, "input", f"{scenario.get_id()}")
        print(target_file)
        _logger.info(f"{scenario.get_id()}: generate end")
        result_queue.put(scenario.get_id())


def player_worker(
    container: ApolloContainer,
    map_service: MapService,
    _logger: Logger,
    task_queue: "mp.Queue[Optional[str]]",
    result_queue: "mp.Queue[Optional[str]]",
    target_dir: Path,
    dry_run: bool,
):
    while True:
        sce_id = task_queue.get()
        if sce_id is None:
            break
        _logger.info(f"{sce_id}: play start ({container.container_name})")
        # TODO: play scenario
        target_input_file = Path(target_dir, "input", f"{sce_id}")
        target_output_path = Path(target_dir, "output", f"{sce_id}")
        print(target_input_file, target_output_path)
        _logger.info(f"{sce_id}: play end")
        result_queue.put(sce_id)


def analysis_worker(
    map_service: MapService,
    _logger: Logger,
    task_queue: "mp.Queue[Optional[str]]",
    result_queue: "mp.Queue[Optional[str]]",
    target_dir: Path,
    dry_run: bool,
):
    while True:
        scenario = task_queue.get()
        if scenario is None:
            break
        _logger.info(f"{scenario}: analysis start")
        target_input_file = Path(target_dir, "output", f"{scenario}.00000")
        print(target_input_file)
        _logger.info(f"{scenario}: analysis end")
        result_queue.put(scenario)
