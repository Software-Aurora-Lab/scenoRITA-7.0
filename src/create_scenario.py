from apollo.container import ApolloContainer
from apollo.utils import change_apollo_map
from config import APOLLO_ROOT, PROJECT_NAME
from pathlib import Path
from apollo.map_service import load_map_service
import time
from typing import Tuple
from datetime import datetime
from scenoRITA.representation import (
    EgoCar,
    Obstacle,
    Scenario,
    ObstacleMotion,
    ObstacleType,
    ObstaclePosition,
    PositionEstimate,
)
from cyber_record.record import Record

from scenoRITA.representation import EgoCar, Obstacle, Scenario
from scenoRITA.components.scenario_generator import ScenarioGenerator


def get_initial_pose_from_record(record_filename: str) -> Tuple[float, float, float]:
    for _, msg, _ in Record(record_filename).read_messages("/apollo/localization/pose"):
        return msg.pose.position.x, msg.pose.position.y, msg.pose.heading
    raise ValueError("No pose message found in record")


def run_scenario(
    container: ApolloContainer,
    input_filename: str,
    output_filename: str,
    scenario_length: int,
    initial_x: float,
    initial_y: float,
    initial_heading: float,
):
    assert container.is_running(), "Container is not running"
    container.stop_ads_modules()
    container.stop_sim_control()
    container.start_sim_control(initial_x, initial_y, initial_heading)
    container.start_ads_modules()
    container.start_recorder(output_filename)
    container.start_replay(input_filename)
    time.sleep(scenario_length)
    container.stop_recorder()
    container.stop_replay()
    container.stop_ads_modules()
    container.stop_sim_control()


ego = EgoCar(
    initial_position=PositionEstimate(lane_id="lane_27", s=35),
    final_position=PositionEstimate(lane_id="lane_29", s=10),
)
obstacle1 = Obstacle(
    id=1,
    initial_position=ObstaclePosition(lane_id="lane_29", index=0),
    final_position=ObstaclePosition(lane_id="lane_29", index=10),
    type=ObstacleType.VEHICLE,
    speed=10,
    width=1.5,
    length=2,
    height=1.5,
    motion=ObstacleMotion.DYNAMIC,
)

obstacle2 = Obstacle(
    id=2,
    initial_position=ObstaclePosition(
        lane_id="",
        index=0,
        x_coord=587049.4405059814,
        y_coord=4141529.948238373,
        z_coord=0.0,
        heading=1.3156606295479158,
    ),
    final_position=ObstaclePosition(lane_id="lane_29", index=0),
    type=ObstacleType.VEHICLE,
    speed=10,
    width=1.5,
    length=2,
    height=1.5,
    motion=ObstacleMotion.STATIC,
)

scenario = Scenario(
    generation_id=0, scenario_id=0, ego_car=ego, obstacles=[obstacle1, obstacle2]
)

map_service = load_map_service("borregas_ave")
scenario_generator = ScenarioGenerator(map_service)
change_apollo_map("borregas_ave")

scenario_length = 30  # seconds
input_record = "scenario.input.00000"
scenario_generator.write_scenario_to_file(
    scenario=scenario,
    filename=input_record,
    scenario_length=scenario_length,
    perception_frequency=10,
)

initial_position, initial_heading = map_service.get_lane_coord_and_heading(
    ego.initial_position.lane_id, ego.initial_position.s
)
initial_x, initial_y = initial_position.x, initial_position.y

# start container
ctn = ApolloContainer(APOLLO_ROOT, f"{PROJECT_NAME}_dev_start")
ctn.start_container(verbose=True)
ctn.start_dreamview()
print(f"Dreamview running at {ctn.dreamview_url}")

# run a scenario
target_docker_dir = Path(f"/{PROJECT_NAME}")
in_docker_path = Path(target_docker_dir, input_record)
in_docker_output = Path(target_docker_dir, datetime.now().strftime("%Y%m%d%H%M%S"))
run_scenario(
    ctn,
    in_docker_path,
    in_docker_output,
    scenario_length,
    initial_x,
    initial_y,
    initial_heading,
)

print("Done")
