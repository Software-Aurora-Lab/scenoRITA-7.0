import multiprocessing as mp
from itertools import repeat
from pathlib import Path

from absl import app, flags
from absl.flags import FLAGS
from cyber_record.record import Record
from shapely.geometry import Polygon

from apollo.utils import generate_adc_polygon, generate_polygon


def get_record_length(record_filename: str, strict=False) -> float:
    try:
        record = Record(record_filename, "r")
    except AttributeError:
        return 0.0
    start_time = record.get_start_time()
    record_length = record.get_end_time() - start_time
    if not strict:
        return record_length / 1e9

    loc = "/apollo/localization/pose"
    pcp = "/apollo/perception/obstacles"
    last_loc = None
    last_pcp = None
    for topic, msg, t in record.read_messages(topics=[loc, pcp]):
        if topic == pcp:
            last_pcp = msg
        elif topic == loc:
            last_loc = msg

        if not (last_loc and last_pcp):
            continue

        ego_x = last_loc.pose.position.x
        ego_y = last_loc.pose.position.y
        ego_pts = generate_adc_polygon(ego_x, ego_y, 0.0, last_loc.pose.heading)
        ego_polygon = Polygon(ego_pts)

        for obstacle in last_pcp.perception_obstacle:
            obs_x = obstacle.position.x
            obs_y = obstacle.position.y
            obs_pts = generate_polygon(
                obs_x, obs_y, 0.0, obstacle.theta, obstacle.length, obstacle.width
            )
            obs_polygon = Polygon(obs_pts)

            if ego_polygon.distance(obs_polygon) == 0.0:
                return (t - start_time) / 1e9

    return record_length / 1e9


def main(argv):
    del argv
    print(FLAGS.dir)
    record_files = list(Path(FLAGS.dir).rglob("*.0000*"))
    total_duration = 0.0

    # for index, record_file in enumerate(record_files):
    #     logger.info(f"Processing {index+1}/{len(record_files)}: {record_file}")
    #     total_duration += get_record_length(record_file, FLAGS.strict)

    with mp.Pool() as pool:
        scenario_lengths = pool.starmap(
            get_record_length, zip(record_files, repeat(FLAGS.strict))
        )
        total_duration = sum(scenario_lengths)

    print(f"Total duration: {total_duration:.2f} seconds")
    total_minutes = total_duration / 60.0
    print(f"Total duration: {total_minutes:.2f} minutes")


if __name__ == "__main__":
    default_dir = "/hdd/apollo-7.0.1/major_revision/AV-FUZZER/12hr_4/simulation/records"
    flags.DEFINE_string("dir", default_dir, "Directory which contain log files")
    flags.DEFINE_boolean(
        "strict", False, "Whether to ignore records after first collision"
    )
    app.run(main)
