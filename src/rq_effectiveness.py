import multiprocessing as mp
import warnings
from pathlib import Path
from typing import List, Optional, Tuple

import pandas as pd
from loguru import logger

from apollo.map_service import load_map_service
from mylib.clustering import cluster_df
from scenoRITA.components.grading_metrics import GradingResult, grade_scenario

AUTOFUZZ_EXPERIMENT_RECORDS = "/home/yuqi/Desktop/Major_Revision/AutoFuzz/1hr_3"
AVFUZZER_EXPERIMENT_RECORDS = "/home/yuqi/Desktop/Major_Revision/AV-FUZZER/12hr_1"

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


def main() -> None:
    exp_root = Path(AUTOFUZZ_EXPERIMENT_RECORDS)
    map_name = "borregas_ave"

    records = list(exp_root.rglob("*.00000"))
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
        violation_order = "CSFHU"
        violations = sorted(
            violation_dfs.keys(), key=lambda x: violation_order.index(x[0])
        )
        for vdf in violations:
            df = violation_dfs[vdf]
            clustered_df = cluster_df(df)
            print(vdf, len(df), len(clustered_df["cluster"].unique()))


if __name__ == "__main__":
    main()
