import multiprocessing as mp
import warnings
from pathlib import Path
from typing import List, Optional, Tuple

import pandas as pd
from absl import app, flags
from loguru import logger

from apollo.map_service import load_map_service
from mylib.clustering import cluster
from scenoRITA.components.grading_metrics import GradingResult, grade_scenario
from utils import PROJECT_ROOT

warnings.filterwarnings("ignore")


def analyze_scenario(
    map_name: str,
    task_queue: "mp.Queue[Optional[Tuple[int, int, Path]]]",
    result_queue: "mp.Queue[GradingResult]",
) -> None:
    map_service = load_map_service(map_name)
    while True:
        record_path = task_queue.get()
        if record_path is None:
            break
        logger.info(f"Processing {record_path[2].name}")
        result = grade_scenario(record_path[2].name, record_path[2], map_service)
        logger.info(f"Finished {record_path[2].name}")
        if result:
            result_queue.put(result)


def check_violations(root: Path, map_name: str) -> None:
    if len(list(root.glob("*.csv"))) > 0:
        # Already processed
        return
    records = list(root.rglob("*.00000"))
    violation_dfs = dict()
    with mp.Manager() as manager:
        worker_num = mp.cpu_count()
        pool = mp.Pool(worker_num)
        task_queue = manager.Queue()
        result_queue = manager.Queue()
        for index, record_path in enumerate(records):
            task_queue.put((0, index, record_path))
        for _ in range(worker_num):
            task_queue.put(None)

        pool.starmap(
            analyze_scenario,
            [(map_name, task_queue, result_queue) for _ in range(worker_num)],
        )
        pool.close()

        results: List[GradingResult] = []
        while not result_queue.empty():
            results.append(result_queue.get())

        for r in results:
            for v in r.violations:
                if v.type not in violation_dfs:
                    violation_dfs[v.type] = pd.DataFrame(
                        columns=["sce_id"] + list(v.features.keys())
                    )
                target_df = violation_dfs[v.type]
                target_df.loc[len(target_df)] = [r.scenario_id] + list(
                    v.features.values()
                )
        for vdf in violation_dfs:
            violation_dfs[vdf].to_csv(Path(root, f"{vdf}.csv"), index=False)


def cluster_violations(root: Path) -> None:
    violation_order = "CSFHU"
    violation_csvs = list(root.glob("*.csv"))

    violation_csvs.sort(key=lambda x: violation_order.index(x.name[0]))
    for csv_file in violation_csvs:
        violation_name = csv_file.name[:-4]
        clustered_df = cluster(csv_file)
        num_violations = len(clustered_df)
        num_clusters = len(clustered_df["cluster"].unique())
        print(violation_name, num_violations, num_clusters)
        out_dir = Path(PROJECT_ROOT, "out")
        out_dir.mkdir(exist_ok=True)
        clustered_df.to_csv(Path(out_dir, f"{violation_name}_out.csv"))


def main(args) -> None:
    del args
    root_dir = Path(flags.FLAGS.dir)
    assert root_dir.exists(), f"{root_dir} does not exist"
    check_violations(root_dir, flags.FLAGS.map)
    cluster_violations(root_dir)


if __name__ == "__main__":
    flags.DEFINE_string("dir", None, "Experiment root directory", required=True)
    flags.DEFINE_string("map", None, "Map name", required=True)
    app.run(main)
