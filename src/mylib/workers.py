import multiprocessing as mp
import time
from logging import Logger
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
    dry_run: bool,
):
    while True:
        scenario = task_queue.get()
        if scenario is None:
            break
        _logger.info(f"{scenario.get_id()}: generate start")
        # TODO: generate scenario
        time.sleep(10)
        _logger.info(f"{scenario.get_id()}: generate end")
        result_queue.put(scenario.get_id())


def player_worker(
    container: ApolloContainer,
    _logger: Logger,
    task_queue: "mp.Queue[Optional[Scenario]]",
    result_queue: mp.Queue,
    dry_run: bool,
):
    while True:
        scenario = task_queue.get()
        if scenario is None:
            break
        _logger.info(f"{scenario}: play start ({container.container_name})")
        # TODO: play scenario
        time.sleep(10)
        _logger.info(f"{scenario}: play end")
        result_queue.put(scenario)


def analysis_worker(
    map_service: MapService,
    _logger: Logger,
    task_queue: mp.Queue,
    result_queue: mp.Queue,
    dry_run: bool,
):
    while True:
        scenario = task_queue.get()
        if scenario is None:
            break
        _logger.info(f"{scenario}: analysis start")
        time.sleep(10)
        _logger.info(f"{scenario}: analysis end")
        result_queue.put(scenario)
