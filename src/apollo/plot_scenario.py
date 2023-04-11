# Inspired by https://www.youtube.com/watch?v=Cj6tAQe7UCY

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
from cyber_record.record import Record
from matplotlib import pyplot as plt
from matplotlib.animation import FFMpegWriter, FuncAnimation
from shapely.geometry import Point

from apollo.map_service import MapService, load_map_service
from apollo.utils import generate_adc_polygon
from config import SUPPORTED_MAPS
from modules.common_msgs.localization_msgs.localization_pb2 import LocalizationEstimate
from modules.common_msgs.perception_msgs.perception_obstacle_pb2 import (
    PerceptionObstacles,
)
from modules.common_msgs.planning_msgs.planning_pb2 import ADCTrajectory


def plot_ego(msg: LocalizationEstimate, radius: int) -> None:
    pos_x = msg.pose.position.x
    pos_y = msg.pose.position.y
    theta = msg.pose.heading
    adc_polygon = generate_adc_polygon(pos_x, pos_y, 0, theta)
    adc_polygon.append(adc_polygon[0])
    plt.plot([p[0] for p in adc_polygon], [p[1] for p in adc_polygon])
    plt.xlim(pos_x - radius, pos_x + radius)
    plt.ylim(pos_y - radius, pos_y + radius)
    plt.arrow(
        pos_x,
        pos_y,
        dx=np.cos(theta),
        dy=np.sin(theta),
        width=0.1,
        color="blue",
        head_starts_at_zero=True,
    )
    vx = msg.pose.linear_velocity.x
    vy = msg.pose.linear_velocity.y
    velocity = np.sqrt(vx**2 + vy**2)
    plt.text(pos_x - radius + 5, pos_y - radius + 5, f"v = {velocity:.2f}")


def plot_planning(msg: Optional[ADCTrajectory]) -> None:
    if msg is None:
        return
    if len(msg.trajectory_point) > 0:
        xes = [p.path_point.x for p in msg.trajectory_point]
        yes = [p.path_point.y for p in msg.trajectory_point]
        plt.plot(xes, yes, color="blue", linewidth=1.0)


def plot_map_lanes(
    pos_x: float, pos_y: float, radius: int, map_service: MapService
) -> None:
    lanes = map_service.get_lanes(Point(pos_x, pos_y), radius)
    # boundary_types = [
    #     "UNKNOWN",
    #     "DOTTED_YELLOW",
    #     "DOTTED_WHITE",
    #     "SOLID_YELLOW",
    #     "SOLID_WHITE",
    #     "DOUBLE_YELLOW",
    #     "CURB",
    # ]
    boundary_style = ["k-", "y--", "k--", "y-", "w-", "y--", "r-"]
    for lane_id in lanes:
        left, right = map_service.get_lane_boundaries_by_id(lane_id)
        ltype, rtype = map_service.get_lane_boundary_types_by_id(lane_id)

        plt.plot(left.xy[0], left.xy[1], boundary_style[ltype])
        plt.plot(right.xy[0], right.xy[1], boundary_style[rtype])


def plot_obstacles(msg: Optional[PerceptionObstacles]) -> None:
    if msg is None:
        return
    # obstacle_types = [
    #     "UNKNOWN",
    #     "UNKNOWN_MOVABLE",
    #     "UNKNOWN_UNMOVABLE",
    #     "PEDESTRIAN",
    #     "BICYCLE",
    #     "VEHICLE",
    # ]
    obstacle_styles = ["k", "k", "k", "y", "b", "g"]

    for obstacle in msg.perception_obstacle:
        obs_type = obstacle.type
        obs_polygon = [(p.x, p.y) for p in obstacle.polygon_point]
        obs_polygon.append(obs_polygon[0])
        xes = [p[0] for p in obs_polygon]
        yes = [p[1] for p in obs_polygon]
        plt.plot(xes, yes, obstacle_styles[obs_type])
        plt.arrow(
            obstacle.position.x,
            obstacle.position.y,
            dx=np.cos(obstacle.theta),
            dy=np.sin(obstacle.theta),
            width=0.1,
            color=obstacle_styles[obs_type],
            head_starts_at_zero=True,
        )
        # vx = obstacle.velocity.x
        # vy = obstacle.velocity.y
        # velocity = np.sqrt(vx * vx + vy * vy)
        # plt.text(obstacle.position.x, obstacle.position.y, f"{velocity:.2f}")


def reduce_msgs(
    cyber_record_path: Path, interested_topics: List[str], fps: int = 10
) -> Dict[str, List]:
    tracked_msgs: Dict[str, List] = {topic: [] for topic in interested_topics}
    timestamps: List[float] = []
    with Record(cyber_record_path, "r") as record:
        for topic, msg, t in record.read_messages():
            if topic != "/apollo/localization/pose" and len(timestamps) == 0:
                # skip messages before first localization
                continue

            if len(timestamps) == 0 or (t > timestamps[-1] + (1.0 / fps) * 1e9):
                timestamps.append(t)
                for it in interested_topics:
                    tracked_msgs[it].append(None)

            for it in interested_topics:
                if topic == it:
                    tracked_msgs[it][-1] = msg

    # fix missing messages
    for topic in tracked_msgs:
        non_null = -1
        for index, msg in enumerate(tracked_msgs[topic]):
            if msg is not None:
                non_null = index
            elif msg is None and non_null >= 0:
                tracked_msgs[topic][index] = tracked_msgs[topic][non_null]
    return tracked_msgs


def plot_scenario(cyber_record_path: Path, map_name: str, output_path: Path):
    assert map_name in SUPPORTED_MAPS
    map_service = load_map_service(map_name)

    interested_topics = [
        "/apollo/localization/pose",
        "/apollo/perception/obstacles",
        "/apollo/planning",
    ]
    fps = 25
    radius = 50

    tracked_msgs = reduce_msgs(cyber_record_path, interested_topics, fps)
    start_time = datetime.fromtimestamp(
        tracked_msgs["/apollo/localization/pose"][0].header.timestamp_sec
    )

    def animate(index: int):
        plt.cla()
        current_time = datetime.fromtimestamp(
            tracked_msgs["/apollo/localization/pose"][index].header.timestamp_sec
        )
        time_delta = current_time - start_time
        plt.title(f"t = {time_delta.total_seconds():.2f}")
        pos_x = tracked_msgs["/apollo/localization/pose"][index].pose.position.x
        pos_y = tracked_msgs["/apollo/localization/pose"][index].pose.position.y
        plot_ego(tracked_msgs["/apollo/localization/pose"][index], radius)
        plot_map_lanes(pos_x, pos_y, radius, map_service)
        plot_planning(tracked_msgs["/apollo/planning"][index])
        plot_obstacles(tracked_msgs["/apollo/perception/obstacles"][index])

    anim = FuncAnimation(
        plt.gcf(),
        animate,
        interval=1000 / fps,
        frames=range(len(tracked_msgs[interested_topics[0]])),
        repeat=False,
    )
    writer = FFMpegWriter(fps=fps)
    anim.save(output_path, writer=writer, dpi=100)


if __name__ == "__main__":
    # print(TEST_RECORD)
    # input_record = Path("/Users/yuqihuai/Downloads/gen_20_sce_17.output.00000")
    # plot_scenario(input_record, "borregas_ave", Path("test.mp4"))
    pass
