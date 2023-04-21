import multiprocessing as mp
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

import numpy as np
from cyber_record.record import Record
from matplotlib import pyplot as plt

from apollo.map_service import load_map_service


@dataclass(slots=True)
class LocationAnalysis:
    ego_locations: List[Tuple[float, float]]
    obs_locations: List[Tuple[float, float]]


def analysis_worker(record_path: Path) -> LocationAnalysis:
    record_file = Record(record_path, "r")
    ego_coordinates: List[Tuple[float, float]] = []
    obs_coordinates: List[Tuple[float, float]] = []

    for topic, msg, t in record_file.read_messages():
        if topic == "/apollo/localization/pose":
            ego_coordinates.append((msg.pose.position.x, msg.pose.position.y))
        elif topic == "/apollo/perception/obstacles":
            for obs in msg.perception_obstacle:
                obs_coordinates.append((obs.position.x, obs.position.y))
    return LocationAnalysis(ego_coordinates, obs_coordinates)


def plot_experiment_heatmap(map_name: str, record_root: Path, output_path: Path):
    plt.cla()
    plt.clf()
    plt.subplot(1, 3, 1)
    map_service = load_map_service(map_name)
    min_x, min_y, max_x, max_y = (
        float("inf"),
        float("inf"),
        float("-inf"),
        float("-inf"),
    )

    for lane_id in map_service.lane_table.keys():
        central_curve = map_service.get_lane_central_curve_by_id(lane_id)
        plt.plot(*central_curve.xy, "k", alpha=0.5)
        minx, miny, maxx, maxy = central_curve.bounds
        min_x = min(min_x, minx)
        min_y = min(min_y, miny)
        max_x = max(max_x, maxx)
        max_y = max(max_y, maxy)

    plt.xticks([])
    plt.yticks([])

    # analyze files
    x_ranges = np.linspace(min_x, max_x, 100)
    y_ranges = np.linspace(min_y, max_y, 100)
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

    plt.subplot(1, 3, 2)
    max_value = np.max(ego_heat_map_values)
    for x1, x2 in zip(x_ranges[:-1], x_ranges[1:]):
        for y1, y2 in zip(y_ranges[:-1], y_ranges[1:]):
            x_index = np.searchsorted(x_ranges, x1)
            y_index = np.searchsorted(y_ranges, y1)
            # alpha = ego_heat_map_values[x_index, y_index] / max_value
            alpha = 1.0 if ego_heat_map_values[x_index, y_index] > 0 else 0.0
            plt.fill([x1, x1, x2, x2], [y1, y2, y2, y1], color="blue", alpha=alpha)
    plt.xticks([])
    plt.yticks([])

    plt.subplot(1, 3, 3)
    max_value = np.max(obs_heat_map_values)
    for x1, x2 in zip(x_ranges[:-1], x_ranges[1:]):
        for y1, y2 in zip(y_ranges[:-1], y_ranges[1:]):
            x_index = np.searchsorted(x_ranges, x1)
            y_index = np.searchsorted(y_ranges, y1)
            # alpha = obs_heat_map_values[x_index, y_index] / max_value
            alpha = 1.0 if obs_heat_map_values[x_index, y_index] > 0 else 0.0
            plt.fill([x1, x1, x2, x2], [y1, y2, y2, y1], color="red", alpha=alpha)
    plt.xticks([])
    plt.yticks([])
    plt.savefig(output_path, bbox_inches="tight")


if __name__ == "__main__":
    avfuzzer_path = "/home/yuqi/Desktop/Major_Revision/AV-FUZZER/12hr_1/simulation/records"
    autofuzz_path = "/home/yuqi/Desktop/Major_Revision/AutoFuzz/1hr_1"

    scenoRITA_sf_path = ""
    scenoRITA_ba_path = ""


    exp_records = [
        ("san_francisco", avfuzzer_path, "avfuzzer"),
        ("san_francisco", scenoRITA_sf_path, "scenoRITA"),
        ("borregas_ave", autofuzz_path, "autofuzz"),
        ("borregas_ave", scenoRITA_ba_path, "scenoRITA")
    ]

    for map_name, record_root, approach_name in exp_records:
        if record_root != "" and Path(record_root).exists():
            print(f"Plotting {map_name} {approach_name}")
            plot_experiment_heatmap(map_name, Path(record_root), f"{map_name}_{approach_name}.png")