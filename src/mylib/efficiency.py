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
        self.sce_gen_tracker: Dict[str, List[datetime]] = defaultdict(list)
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
            self.sce_gen_tracker[result.groups()[0]].append(time)
        elif result := re.search(sce_gen_end, line):
            self.sce_gen_tracker[result.groups()[0]].append(time)
        elif result := re.search(sce_play_start, line):
            self.sce_play_tracker[result.groups()[0]].append(time)
        elif result := re.search(sce_play_end, line):
            self.sce_play_tracker[result.groups()[0]].append(time)
        elif result := re.search(sce_analysis_start, line):
            self.sce_analysis_tracker[result.groups()[0]].append(time)
        elif result := re.search(sce_analysis_end, line):
            self.sce_analysis_tracker[result.groups()[0]].append(time)
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

    def parse(self) -> None:
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
    
    def print_header(self, header: str):
        print('='*len(header))
        print(header)
        print('='*len(header))

    def print_stats(self):
        self.print_header(" Stats Per Scenario ")
        self.print_dict_stats("sce_gen", self.sce_gen_tracker)
        self.print_dict_stats("sce_play", self.sce_play_tracker)
        self.print_dict_stats("sce_analysis", self.sce_analysis_tracker)
        self.print_header(" Stats Per Generation ")
        self.print_dict_stats("gen", self.gen_tracker)
        self.print_dict_stats("gen_mut", self.gen_mut_tracker)
        self.print_dict_stats("gen_eval", self.gen_eval_tracker)
        self.print_dict_stats("gen_select", self.gen_select_tracker)


def main():
    filename = "/Users/yuqihuai/ResearchWorkspace/scenoRITA-V3/out/0417_200109_borregas_ave/scenoRITA_V3.log"
    parser = LogParser(Path(filename))
    parser.parse()
    parser.print_stats()


if __name__ == "__main__":
    main()
