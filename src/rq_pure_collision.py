from pathlib import Path
from typing import Optional

from cyber_record.record import Record
from loguru import logger
from shapely.geometry import LineString, Point, Polygon

from apollo.map_service import MapService, load_map_service
from apollo.utils import (
    generate_adc_front_vertices,
    generate_adc_polygon,
    generate_adc_rear_vertices,
)


def analyze_record(map_service: MapService, record_filename: str) -> Optional[str]:
    # Do something with the record
    record = Record(record_filename, "r")
    localization_topic = "/apollo/localization/pose"
    perception_obstacle_topic = "/apollo/perception/obstacles"

    last_localization = None
    last_perception = None
    for topic, msg, t in record.read_messages(
        topics=[localization_topic, perception_obstacle_topic]
    ):
        if topic == localization_topic:
            last_localization = msg
        elif topic == perception_obstacle_topic:
            last_perception = msg

        if last_localization is None or last_perception is None:
            continue

        # begin analyze
        ego_x = last_localization.pose.position.x
        ego_y = last_localization.pose.position.y
        ego_theta = last_localization.pose.heading
        ego_polygon = generate_adc_polygon(ego_x, ego_y, 0.0, ego_theta)
        ego_p = Polygon(ego_polygon)
        ego_front = generate_adc_front_vertices(ego_x, ego_y, 0.0, ego_theta)
        ego_front_l = LineString(ego_front)
        ego_rear = generate_adc_rear_vertices(ego_x, ego_y, 0.0, ego_theta)
        ego_rear_l = LineString(ego_rear)

        for obs in last_perception.perception_obstacle:
            obs_x = obs.position.x
            obs_y = obs.position.y
            obs_theta = obs.theta
            obs_polygon = generate_adc_polygon(obs_x, obs_y, 0.0, obs_theta)
            obs_p = Polygon(obs_polygon)
            if ego_p.intersects(obs_p):
                # collision detected
                if ego_rear_l.intersects(obs_p):
                    return "Rear-End Collision"
                obs_lane = map_service.get_lanes(Point(obs_x, obs_y), 10.0)
                obs_in_lane = False
                for lane_id in obs_lane:
                    lboundary, rboundary = map_service.get_lane_boundaries_by_id(
                        lane_id
                    )
                    lx, ly = lboundary.xy
                    rx, ry = rboundary.xy
                    x_es = lx + rx[::-1]
                    y_es = ly + ry[::-1]
                    lane_polygon = Polygon(zip(x_es, y_es))
                    if (
                        lane_polygon.intersects(obs_p)
                        and abs(lane_polygon.intersection(obs_p).area - obs_p.area)
                        < 1e-3
                    ):
                        obs_in_lane = True
                        break
                if not obs_in_lane:
                    return "Side Collision (Not in Lane)"

                if ego_front_l.intersects(obs_p):
                    return "Front Collision"

                raise Exception(f"Unknown collision type for record {record_filename}")
    return None


def main():
    map_name = "san_francisco"
    map_service = load_map_service(map_name)
    experiment_directory = "/hdd/apollo-7.0.1/major_revision/AV-FUZZER/12hr_1"

    collision_counter = dict()
    record_files = list(Path(experiment_directory).rglob("*.00000"))
    for index, record_file in enumerate(record_files):
        logger.info(f"Working on {index+1}/{len(record_files)}")
        collision_type = analyze_record(map_service, record_file)
        if collision_type:
            collision_counter[collision_type] = (
                collision_counter.get(collision_type, 0) + 1
            )

    print(collision_counter)


if __name__ == "__main__":
    main()
