import multiprocessing as mp
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Set, Tuple

import matplotlib as mpl
import numpy as np
from cyber_record.record import Record
from loguru import logger
from matplotlib import pyplot as plt

from apollo.map_service import load_map_service

mpl.rcParams["figure.dpi"] = 900


@dataclass(slots=True)
class LocationAnalysis:
    ego_locations: Set[Tuple[float, float]]
    obs_locations: Set[Tuple[float, float]]


def get_color(alpha: float):
    colors = [
        "#ffffff",
        "#eaf8f2",
        "#a1ddea",
        "#61bdf7",
        "#4f8ba3",
        "#9e5bd5",
        "#c72e7d",
    ]
    values = np.linspace(0.0, 1.0, len(colors))
    return colors[np.searchsorted(values, alpha)]


def analysis_worker(record_path: Path) -> LocationAnalysis:
    logger.info(f"Processing {record_path.name}")
    record_file = Record(record_path, "r")
    ego_coordinates: Set[Tuple[float, float]] = set()
    obs_coordinates: Set[Tuple[float, float]] = set()

    for topic, msg, t in record_file.read_messages():
        if topic == "/apollo/localization/pose":
            ego_coord = (msg.pose.position.x, msg.pose.position.y)
            ego_coordinates.add(ego_coord)
        elif topic == "/apollo/perception/obstacles":
            for obs in msg.perception_obstacle:
                obs_coord = (obs.position.x, obs.position.y)
                obs_coordinates.add(obs_coord)
    return LocationAnalysis(ego_coordinates, obs_coordinates)


def plot_experiment_heatmap(map_name: str, record_root: Path, output_path: Path):
    plt.cla()
    plt.clf()
    map_service = load_map_service(map_name)
    min_x, min_y, max_x, max_y = (
        float("inf"),
        float("inf"),
        float("-inf"),
        float("-inf"),
    )

    # plot map for 2 subplots
    for i in range(1, 3):
        plt.subplot(1, 2, i)
        for lane_id in map_service.lane_table.keys():
            central_curve = map_service.get_lane_central_curve_by_id(lane_id)
            plt.plot(*central_curve.xy, "k", alpha=0.1)
            minx, miny, maxx, maxy = central_curve.bounds
            min_x = min(min_x, minx)
            min_y = min(min_y, miny)
            max_x = max(max_x, maxx)
            max_y = max(max_y, maxy)
        plt.xticks([])
        plt.yticks([])

    # analyze files
    k_split = 100
    x_ranges = np.linspace(min_x, max_x, k_split)
    y_ranges = np.linspace(min_y, max_y, k_split)
    ego_heat_map_values = np.zeros((len(x_ranges) + 1, len(y_ranges) + 1))
    obs_heat_map_values = np.zeros((len(x_ranges) + 1, len(y_ranges) + 1))

    with mp.Pool(mp.cpu_count()) as pool:
        results = pool.map(analysis_worker, record_root.rglob("*.00000"))
        for result in results:
            for ego_coord in result.ego_locations:
                x_index = np.searchsorted(x_ranges, ego_coord[0])
                y_index = np.searchsorted(y_ranges, ego_coord[1])
                ego_heat_map_values[x_index, y_index] += 1
            for obs_coord in result.obs_locations:
                x_index = np.searchsorted(x_ranges, obs_coord[0])
                y_index = np.searchsorted(y_ranges, obs_coord[1])
                obs_heat_map_values[x_index, y_index] += 1

    # plot heat map for ego car
    plt.subplot(1, 2, 1)
    max_value = np.max(ego_heat_map_values)
    min_alpha = 0.5
    for x1, x2 in zip(x_ranges[:-1], x_ranges[1:]):
        x_index = np.searchsorted(x_ranges, (x1 + x2) / 2)
        for y1, y2 in zip(y_ranges[:-1], y_ranges[1:]):
            y_index = np.searchsorted(y_ranges, (y1 + y2) / 2)
            alpha = ego_heat_map_values[x_index, y_index] / max_value
            color = get_color(alpha)

            color = "blue"
            if alpha > 0.0:
                # scale alpha to make it more visible
                alpha = min_alpha + alpha * (1 - min_alpha)

            plt.fill([x1, x1, x2, x2], [y1, y2, y2, y1], color=color, alpha=alpha)

    # plot heat map for obstacles
    plt.subplot(1, 2, 2)
    max_value = np.max(obs_heat_map_values)
    for x1, x2 in zip(x_ranges[:-1], x_ranges[1:]):
        x_index = np.searchsorted(x_ranges, (x1 + x2) / 2)
        for y1, y2 in zip(y_ranges[:-1], y_ranges[1:]):
            y_index = np.searchsorted(y_ranges, (y1 + y2) / 2)
            alpha = obs_heat_map_values[x_index, y_index] / max_value
            color = get_color(alpha)

            color = "red"
            if alpha > 0.0:
                # scale alpha to make it more visible
                alpha = min_alpha + alpha * (1 - min_alpha)

            plt.fill([x1, x1, x2, x2], [y1, y2, y2, y1], color=color, alpha=alpha)

    # save figure
    plt.savefig(output_path, bbox_inches="tight")


if __name__ == "__main__":
    avfuzzer_path = (
        "/home/yuqi/Desktop/Major_Revision/AV-FUZZER/12hr_1/simulation/records"
    )
    autofuzz_path = "/home/yuqi/Desktop/Major_Revision/AutoFuzz/1hr_1"

    scenoRITA_sf_path = (
        "/home/yuqi/ResearchWorkspace/scenoRITA-V3/out/0424_130519_san_francisco"
    )
    scenoRITA_ba_path = (
        "/home/yuqi/ResearchWorkspace/scenoRITA-V3/out/0424_213748_borregas_ave"
    )

    exp_records = [
        # ("san_francisco", avfuzzer_path, "avfuzzer"),
        # ("borregas_ave", autofuzz_path, "autofuzz"),
        # ("san_francisco", scenoRITA_sf_path, "scenoRITA"),
        ("borregas_ave", scenoRITA_ba_path, "scenoRITA"),
    ]

    for map_name, record_root, approach_name in exp_records:
        if record_root != "" and Path(record_root).exists():
            start = time.perf_counter()
            logger.info(f"Plotting {map_name} {approach_name}")
            plot_experiment_heatmap(
                map_name, Path(record_root), Path(f"{map_name}_{approach_name}.png")
            )
            minutes = (time.perf_counter() - start) / 60
            logger.info(f"Finished {map_name} {approach_name} in {minutes:.2f} minutes")
