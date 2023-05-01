import math
import shutil
from pathlib import Path
from typing import List, Tuple

from config import APOLLO_FLAGFILE, APOLLO_ROOT, MAPS_DIR, SUPPORTED_MAPS

USING_LGSVL = True
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


def change_apollo_map(map_name: str) -> None:
    """
    Change the map used by Apollo
    :param str map_name: name of the map to use
    """
    assert map_name in SUPPORTED_MAPS, f"Unsupported map: {map_name}"
    APOLLO_FLAGFILE.parent.mkdir(parents=True, exist_ok=True)
    with open(APOLLO_FLAGFILE, "a") as fp:
        fp.write(f"\n--map_dir=/apollo/modules/map/data/{map_name}\n")

    apollo_map_dir = Path(APOLLO_ROOT, "modules", "map", "data", map_name)
    apollo_map_dir.parent.mkdir(parents=True, exist_ok=True)
    if not apollo_map_dir.exists():
        shutil.copytree(
            Path(MAPS_DIR, map_name),
            apollo_map_dir,
        )


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
