import math
import shutil
from pathlib import Path
from typing import List, Tuple
from nanoid import generate as nanoid_generate

from apollo.container import ApolloContainer
from config import APOLLO_FLAGFILE, APOLLO_ROOT, MAPS_DIR

USING_LGSVL = False
APOLLO_VEHICLE_LENGTH = 4.933
"""Length of default Apollo vehicle"""
APOLLO_VEHICLE_WIDTH = 2.11
"""Width of default Apollo vehicle"""
APOLLO_VEHICLE_HEIGHT = 1.48
"""Height of default Apollo vehicle"""
APOLLO_VEHICLE_back_edge_to_center = 1.043
"""Length between the back edge and the center of default Apollo vehicle"""

if USING_LGSVL:
    APOLLO_VEHICLE_LENGTH = 4.70
    APOLLO_VEHICLE_WIDTH = 2.06
    APOLLO_VEHICLE_HEIGHT = 2.05
    APOLLO_VEHICLE_back_edge_to_center = 0.995


def clean_apollo_logs():
    data_dir = Path(APOLLO_ROOT, "data")
    if data_dir.exists():
        shutil.rmtree(data_dir)
    for log_file in APOLLO_ROOT.glob("*.log.*"):
        log_file.unlink()


def change_apollo_map(ctn: ApolloContainer, map_name: str) -> Tuple[str, Path]:
    """
    Change the map used by Apollo
    :param str map_name: name of the map to use
    """
    assert ctn.is_running(), "Apollo container is not running"
    map_bin = Path(MAPS_DIR, map_name, "base_map.bin")
    assert map_bin.exists(), f"Map binary file not found: {map_bin}"
    
    # copy map binary to Apollo container
    dst_map_id = ""
    while True:
        dst_map_id = "scenoRITA_" + \
            nanoid_generate("abcdefghijklmnopqrstuvwxyz0123456789", size=10)
        if not (Path(APOLLO_ROOT, "data", dst_map_id).exists()):
            break
    
    APOLLO_FLAGFILE.parent.mkdir(parents=True, exist_ok=True)
    with open(APOLLO_FLAGFILE, "a") as fp:
        fp.write(f"\n--map_dir=/apollo/modules/map/data/{dst_map_id}\n")

    dst_map_path = Path(APOLLO_ROOT, "modules", "map", "data", dst_map_id)
    dst_map_path.mkdir(parents=True, exist_ok=True)

    in_docker_map_path = Path("/apollo/modules/map/data", dst_map_id)
    # copy map binary to apollo folder
    shutil.copy(map_bin, dst_map_path)
    ctn.exec(f"bash /apollo/scripts/generate_routing_topo_graph.sh"
             f" --map_dir {in_docker_map_path}")
    ctn.exec(f"bazel-bin/modules/map/tools/sim_map_generator "
             f"--map_dir={in_docker_map_path} "
             f"--output_dir={in_docker_map_path}")
    # check if map binary is generated successfully
    if not Path(dst_map_path, "base_map.bin").exists():
        raise FileNotFoundError(f"Failed to copy map binary in {dst_map_path}")
    if not Path(dst_map_path, "routing_map.bin").exists():
        raise FileNotFoundError(f"Failed to generate routing map binary in {dst_map_path}")
    if not Path(dst_map_path, "sim_map.bin").exists():
        raise FileNotFoundError(f"Failed to generate sim map binary in {dst_map_path}")
    return dst_map_id, dst_map_path


def generate_polygon(
    pos_x: float, pos_y: float, pos_z: float, theta: float, length: float, width: float
) -> List[Tuple[float, float, float]]:
    """
    Generate polygon for a perception obstacle
    :param float pos_x: x position of the obstacle
    :param float pos_y: y position of the obstacle
    :param float pos_z: z position of the obstacle
    :param float theta: heading of the obstacle
    :param float length: length of the obstacle
    :param float width: width of the obstacle
    :return: list of points
    """
    points: List[Tuple[float, float, float]] = []
    half_l = length / 2.0
    half_w = width / 2.0
    sin_h = math.sin(theta)
    cos_h = math.cos(theta)
    vectors = [
        (half_l * cos_h - half_w * sin_h, half_l * sin_h + half_w * cos_h),
        (-half_l * cos_h - half_w * sin_h, -half_l * sin_h + half_w * cos_h),
        (-half_l * cos_h + half_w * sin_h, -half_l * sin_h - half_w * cos_h),
        (half_l * cos_h + half_w * sin_h, half_l * sin_h - half_w * cos_h),
    ]
    for x, y in vectors:
        points.append((pos_x + x, pos_y + y, pos_z))
    return points


def generate_adc_polygon(
    pos_x: float, pos_y: float, pos_z: float, theta: float
) -> List[Tuple[float, float, float]]:
    """
    Generate a polygon for the ADC based on its current position
    :param float pos_x: x position of the ADC
    :param float pos_y: y position of the ADC
    :param float pos_z: z position of the ADC
    :param float theta: the heading of the ADC (in radians)
    :returns: a list consisting 4 tuples to represent the polygon of the ADC
    """

    points = []
    half_w = APOLLO_VEHICLE_WIDTH / 2.0
    front_l = APOLLO_VEHICLE_LENGTH - APOLLO_VEHICLE_back_edge_to_center
    back_l = -1 * APOLLO_VEHICLE_back_edge_to_center
    sin_h = math.sin(theta)
    cos_h = math.cos(theta)
    vectors = [
        (front_l * cos_h - half_w * sin_h, front_l * sin_h + half_w * cos_h),
        (back_l * cos_h - half_w * sin_h, back_l * sin_h + half_w * cos_h),
        (back_l * cos_h + half_w * sin_h, back_l * sin_h - half_w * cos_h),
        (front_l * cos_h + half_w * sin_h, front_l * sin_h - half_w * cos_h),
    ]
    for x, y in vectors:
        points.append((pos_x + x, pos_y + y, pos_z))
    return points


def generate_adc_rear_vertices(
    pos_x: float, pos_y: float, pos_z: float, theta: float
) -> List[Tuple[float, float, float]]:
    """
    Generate the rear edge for the ADC
    :param float pos_x: x position of the ADC
    :param float pos_y: y position of the ADC
    :param float pos_z: z position of the ADC
    :param float theta: the heading of the ADC (in radians)
    :returns: a list consisting 2 tuples to represent the rear edge of the ADC
    """
    points = []
    half_w = APOLLO_VEHICLE_WIDTH / 2.0
    back_l = -1 * APOLLO_VEHICLE_back_edge_to_center
    sin_h = math.sin(theta)
    cos_h = math.cos(theta)
    vectors = [
        (back_l * cos_h - half_w * sin_h, back_l * sin_h + half_w * cos_h),
        (back_l * cos_h + half_w * sin_h, back_l * sin_h - half_w * cos_h),
    ]

    for x, y in vectors:
        points.append((pos_x + x, pos_y + y, pos_z))
    return points


def generate_adc_front_vertices(
    pos_x: float, pos_y: float, pos_z: float, theta: float
) -> List[Tuple[float, float, float]]:
    """
    Generate the rear edge for the ADC
    :param float pos_x: x position of the ADC
    :param float pos_y: y position of the ADC
    :param float pos_z: z position of the ADC
    :param float theta: the heading of the ADC (in radians)
    :returns: a list consisting 2 tuples to represent the rear edge of the ADC
    """
    points = []
    half_w = APOLLO_VEHICLE_WIDTH / 2.0
    front_l = APOLLO_VEHICLE_LENGTH - APOLLO_VEHICLE_back_edge_to_center
    sin_h = math.sin(theta)
    cos_h = math.cos(theta)
    vectors = [
        (front_l * cos_h - half_w * sin_h, front_l * sin_h + half_w * cos_h),
        (front_l * cos_h + half_w * sin_h, front_l * sin_h - half_w * cos_h),
    ]

    for x, y in vectors:
        points.append((pos_x + x, pos_y + y, pos_z))
    return points
