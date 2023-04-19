import os
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import numpy as np

LOGGING_PREFIX_REGEX = (
    "^(?P<severity>[DIWEF])(?P<month>\d\d)(?P<day>\d\d) "
    "(?P<hour>\d\d):(?P<minute>\d\d):(?P<second>\d\d)\.(?P<microsecond>\d\d\d) "
    "(?P<filename>[a-zA-Z<][\w._<>-]+):(?P<line>\d+)"
)


class LogParser:
    def __init__(self, filename: Path) -> None:
        self.filename = filename
        self.map_name: str
        self.sce_tracker: Dict[str, List[datetime]] = defaultdict(list)
        self.sce_generate_tracker: Dict[str, List[datetime]] = defaultdict(list)
        self.sce_play_tracker: Dict[str, List[datetime]] = defaultdict(list)
        self.sce_analysis_tracker: Dict[str, List[datetime]] = defaultdict(list)
        self.gen_tracker: Dict[str, List[datetime]] = defaultdict(list)
        self.gen_mut_tracker: Dict[str, List[datetime]] = defaultdict(list)
        self.gen_eval_tracker: Dict[str, List[datetime]] = defaultdict(list)
        self.gen_select_tracker: Dict[str, List[datetime]] = defaultdict(list)

    def parse_line(self, time: datetime, line: str) -> None:
        sce_gen_start = r"(gen_\d+_sce_\d+): generate start"
        sce_gen_end = r"(gen_\d+_sce_\d+): generate end"
        sce_play_start = r"(gen_\d+_sce_\d+): play start"
        sce_play_end = r"(gen_\d+_sce_\d+): play end"
        sce_analysis_start = r"(gen_\d+_sce_\d+): analysis start"
        sce_analysis_end = r"(gen_\d+_sce_\d+): analysis end"
        gen_start = r"(Generation \d+): start"
        gen_mut = r"(Generation \d+): mut/cx done"
        gen_eval = r"(Generation \d+): evaluation done"
        gen_select = r"(Generation \d+): selection done"
        gen_end = r"(Generation \d+): end"

        if result := re.search(sce_gen_start, line):
            self.sce_generate_tracker[result.groups()[0]].append(time)
            self.sce_tracker[result.groups()[0]].append(time)
        elif result := re.search(sce_gen_end, line):
            self.sce_generate_tracker[result.groups()[0]].append(time)
        elif result := re.search(sce_play_start, line):
            self.sce_play_tracker[result.groups()[0]].append(time)
        elif result := re.search(sce_play_end, line):
            self.sce_play_tracker[result.groups()[0]].append(time)
        elif result := re.search(sce_analysis_start, line):
            self.sce_analysis_tracker[result.groups()[0]].append(time)
        elif result := re.search(sce_analysis_end, line):
            self.sce_analysis_tracker[result.groups()[0]].append(time)
            self.sce_tracker[result.groups()[0]].append(time)
        elif result := re.search(gen_start, line):
            self.gen_tracker[result.groups()[0]].append(time)
            self.gen_mut_tracker[result.groups()[0]].append(time)
        elif result := re.search(gen_mut, line):
            self.gen_mut_tracker[result.groups()[0]].append(time)
            self.gen_eval_tracker[result.groups()[0]].append(time)
        elif result := re.search(gen_eval, line):
            self.gen_eval_tracker[result.groups()[0]].append(time)
            self.gen_select_tracker[result.groups()[0]].append(time)
        elif result := re.search(gen_select, line):
            self.gen_select_tracker[result.groups()[0]].append(time)
        elif result := re.search(gen_end, line):
            self.gen_tracker[result.groups()[0]].append(time)
        else:
            pass

    def parse_map_name(self) -> None:
        map_name = self.filename.resolve().parts[-1].split(".")[0]
        self.map_name = " ".join([i.capitalize() for i in map_name.split("_")])
        # map_part = self.filename.resolve().parts[-2]
        # match = re.match("\d+_\d+_(.*)", map_part)
        # if match:
        #     map_name = match.groups()[0]
        #     self.map_name = " ".join([i.capitalize() for i in map_name.split("_")])

    def parse(self) -> None:
        self.parse_map_name()

        with open(self.filename, "r") as fp:
            while True:
                line = fp.readline()
                if not line:
                    break
                line = line.strip()
                match = re.match(LOGGING_PREFIX_REGEX, line)
                if not match:
                    continue

                group_dict = match.groupdict()
                msg_time = datetime(
                    year=2023,
                    month=int(group_dict["month"]),
                    day=int(group_dict["day"]),
                    hour=int(group_dict["hour"]),
                    minute=int(group_dict["minute"]),
                    second=int(group_dict["second"]),
                    microsecond=int(group_dict["microsecond"]),
                )
                self.parse_line(msg_time, line[match.span()[1] + 2 :])

    def print_dict_stats(self, name: str, D: dict):
        values = []
        for _, value in D.items():
            if len(value) == 2:
                values.append((value[1] - value[0]).total_seconds())
        print(
            f"{name}: {np.mean(values):.2f} "
            f"+- {np.std(values):.2f} ({len(values)} samples)"
        )

    def get_mean_value(self, D: dict):
        values = []
        for _, value in D.items():
            if len(value) == 2:
                values.append((value[1] - value[0]).total_seconds())
        return np.mean(values)

    def print_header(self, header: str):
        print("=" * len(header))
        print(header)
        print("=" * len(header))

    def print_stats(self):
        self.print_header(" Stats Per Scenario ")
        self.print_dict_stats("sce_e2e", self.sce_tracker)
        self.print_dict_stats("sce_generate", self.sce_generate_tracker)
        self.print_dict_stats("sce_play", self.sce_play_tracker)
        self.print_dict_stats("sce_analysis", self.sce_analysis_tracker)
        self.print_header(" Stats Per Generation ")
        self.print_dict_stats("gen_e2e", self.gen_tracker)
        self.print_dict_stats("gen_mut", self.gen_mut_tracker)
        self.print_dict_stats("gen_eval", self.gen_eval_tracker)
        self.print_dict_stats("gen_select", self.gen_select_tracker)

    def output_latex(self, fp):
        fp.write("            \\textbf{" + self.map_name + "}")
        time_list = [
            self.get_mean_value(tracker)
            for tracker in [
                self.sce_generate_tracker,
                self.sce_play_tracker,
                self.sce_analysis_tracker,
                self.gen_mut_tracker,
                self.gen_eval_tracker,
                self.gen_select_tracker,
                self.gen_tracker,
            ]
        ]
        time_list.insert(3, np.sum(time_list[0:3]))
        for time in time_list:
            fp.write(" & " + f"{time:.2f}")
        fp.write(" \\\\\n")


def main():
    out_dir = Path("/home/cloudsky/Research/Apollo/scenoRITA-V3/out")
    # log_files = [f"{out_dir}/{i}/scenoRITA_V3.log" for i in os.listdir(out_dir) if os.path.isdir(f"{out_dir}/{i}")]
    log_dir = f"{out_dir}/logs"
    log_files = [f"{log_dir}/{i}" for i in os.listdir(log_dir)]

    # or
    # log_files = ["/home/cloudsky/Research/Apollo/scenoRITA-V3/out/0417_211736_borregas_ave/scenoRITA_V3.log",
    #              "/home/cloudsky/Research/Apollo/scenoRITA-V3/out/0418_101510_borregas_ave/scenoRITA_V3.log"]

    with open(f"{out_dir}/out.txt", "w") as fp:
        for log_file in log_files:
            parser = LogParser(Path(log_file))
            parser.parse()
            parser.print_stats()
            parser.output_latex(fp)


if __name__ == "__main__":
    main()
