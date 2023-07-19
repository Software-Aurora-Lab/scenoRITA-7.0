from apollo.container import ApolloContainer
from config import APOLLO_ROOT, PROJECT_NAME
from pathlib import Path
from apollo.map_service import load_map_service
import time
from typing import Tuple
from datetime import datetime

from cyber_record.record import Record


def get_initial_pose_from_record(record_filename: str) -> Tuple[float, float, float]:
    for _, msg, _ in Record(record_filename).read_messages("/apollo/localization/pose"):
        return msg.pose.position.x, msg.pose.position.y, msg.pose.heading
    raise ValueError("No pose message found in record")


def run_scenario(
    container: ApolloContainer,
    input_filename: str,
    output_filename: str,
    scenario_length: int,
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


input_record = "asd.record"
assert Path(input_record).exists(), f"Input record {input_record} does not exist"

map_service = load_map_service("borregas_ave")
scenario_length = 30
initial_x, initial_y, initial_heading = get_initial_pose_from_record(input_record)

# start container
ctn = ApolloContainer(APOLLO_ROOT, f"{PROJECT_NAME}_dev_start")
ctn.start_container()
ctn.start_dreamview()
print(f"Dreamview running at {ctn.dreamview_url}")

# run a scenario
target_docker_dir = Path(f"/{PROJECT_NAME}")
in_docker_path = Path(target_docker_dir, input_record)
in_docker_output = Path(target_docker_dir, datetime.now.strftime("%Y%m%d%H%M%S"))
run_scenario(ctn, in_docker_path, in_docker_output, scenario_length)

print("Done")
