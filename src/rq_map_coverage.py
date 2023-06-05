import time
from pathlib import Path
from typing import Dict, Set, Tuple

from cyber_record.record import Record
from loguru import logger
from shapely.geometry import LineString, Point, Polygon

from apollo.map_service import load_map_service


def compute_coverage(map_name: str, record_root: Path):
    record_files = sorted(record_root.rglob("*.00000"))
    map_service = load_map_service(map_name)

    # initialize junction polygons, signal lines and stop sign lines
    junction_polygons: Dict[str, Polygon] = dict()
    signal_lines: Dict[str, LineString] = dict()
    unique_signal_lines: Set[LineString] = set()
    stop_sign_lines: Dict[str, LineString] = dict()
    unique_stop_sign_lines: Set[LineString] = set()

    # Build junction polygons, signal lines and stop sign lines
    for junction_id in map_service.junction_table.keys():
        junction = map_service.junction_table[junction_id]
        junction_polygon = Polygon([(x.x, x.y) for x in junction.polygon.point])
        junction_polygons[junction_id] = junction_polygon

    for signal_id in map_service.signal_table.keys():
        signal = map_service.signal_table[signal_id]
        signal_linestring = LineString(
            [(x.x, x.y) for x in signal.stop_line[0].segment[0].line_segment.point]
        )
        if signal_linestring not in unique_signal_lines:
            unique_signal_lines.add(signal_linestring)
            signal_lines[signal_id] = signal_linestring
        else:
            logger.warning(f"Duplicate signal {signal_id}")

    for stop_sign_id in map_service.stop_sign_table.keys():
        stop_sign = map_service.stop_sign_table[stop_sign_id]
        stop_sign_linestring = LineString(
            [(x.x, x.y) for x in stop_sign.stop_line[0].segment[0].line_segment.point]
        )
        if stop_sign_linestring not in unique_stop_sign_lines:
            unique_stop_sign_lines.add(stop_sign_linestring)
            stop_sign_lines[stop_sign_id] = stop_sign_linestring
        else:
            logger.warning(f"Duplicate stop sign {stop_sign_id}")

    # initialize coverage dictionaries
    junction_coverage: Dict[str, int] = dict()
    signal_coverage: Dict[str, int] = dict()
    stop_sign_coverage: Dict[str, int] = dict()

    # compute coverage for each record
    for index, record_file in enumerate(record_files):
        logger.info(f"Processing {record_file.name} ({index + 1}/{len(record_files)})")

        ego_lanes: Set[str] = set()
        # construct ego trajectory line string
        ego_coordinates: Set[Tuple[float, float]] = set()
        record = Record(record_file, "r")
        for _, msg, _ in record.read_messages("/apollo/localization/pose"):
            ego_coord = (msg.pose.position.x, msg.pose.position.y)
            ego_coordinates.add(ego_coord)
            ego_lane = map_service.get_nearest_lanes_with_heading(
                Point(*ego_coord), msg.pose.heading
            )
            ego_lanes.add(ego_lane[0])
        if len(ego_coordinates) < 2:
            logger.warning(f"Record {record_file.name} has less than 2 coordinates")
            continue
        ego_lst = LineString(ego_coordinates)

        ego_lane_overlap_ids: Set[str] = set()
        for el in ego_lanes:
            ego_lane_overlap_ids |= set(
                [x.id for x in map_service.lane_table[el].overlap_id]
            )

        # compute coverage for junctions, signals and stop signs
        for junction_id, junction_polygon in junction_polygons.items():
            if junction_polygon.intersects(ego_lst):
                if junction_id not in junction_coverage:
                    junction_coverage[junction_id] = 1
                else:
                    junction_coverage[junction_id] += 1

        for signal_id, signal_linestring in signal_lines.items():
            if signal_linestring.intersects(ego_lst):
                signal_overlap_ids = [
                    x.id for x in map_service.signal_table[signal_id].overlap_id
                ]
                if set(ego_lane_overlap_ids) & set(signal_overlap_ids):
                    if signal_id not in signal_coverage:
                        signal_coverage[signal_id] = 1
                    else:
                        signal_coverage[signal_id] += 1

        for stop_sign_id, stop_sign_linestring in stop_sign_lines.items():
            if stop_sign_linestring.intersects(ego_lst):
                stop_sign_overlap_ids = [
                    x.id for x in map_service.stop_sign_table[stop_sign_id].overlap_id
                ]
                if set(ego_lane_overlap_ids) & set(stop_sign_overlap_ids):
                    if stop_sign_id not in stop_sign_coverage:
                        stop_sign_coverage[stop_sign_id] = 1
                    else:
                        stop_sign_coverage[stop_sign_id] += 1

    # print coverage results
    print(f"Number of junctions: {len(junction_polygons)}")
    print(f"Number of junctions covered: {len(junction_coverage)}")
    print(f"Number of signals: {len(signal_lines)}")
    print(f"Number of signals covered: {len(signal_coverage)}")
    print(f"Number of stop signs: {len(stop_sign_lines)}")
    print(f"Number of stop signs covered: {len(stop_sign_coverage)}")


if __name__ == "__main__":
    avfuzzer_path = (
        "/hdd/apollo-7.0.1/major_revision/AV-FUZZER/12hr_1/simulation/records"
    )
    autofuzz_path = "/hdd/apollo-7.0.1/major_revision/AutoFuzz/1hr_1"

    scenoRITA_sf_path = "/home/yuqi/ResearchWorkspace/scenoRITA-V3/out/0507_165932_san_francisco/records"
    scenoRITA_ba_path = (
        "/home/yuqi/ResearchWorkspace/scenoRITA-V3/out/0424_213748_borregas_ave"
    )

    exp_records = [
        # ("san_francisco", avfuzzer_path, "avfuzzer"),
        # ("borregas_ave", autofuzz_path, "autofuzz"),
        ("san_francisco", scenoRITA_sf_path, "scenoRITA"),
        # ("borregas_ave", scenoRITA_ba_path, "scenoRITA"),
    ]

    for map_name, record_root, approach_name in exp_records:
        if record_root != "" and Path(record_root).exists():
            start = time.perf_counter()
            compute_coverage(map_name, Path(record_root))
            minutes = (time.perf_counter() - start) / 60
            logger.info(f"Finished {map_name} {approach_name} in {minutes:.2f} minutes")
