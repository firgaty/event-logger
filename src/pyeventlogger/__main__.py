import argparse
import pathlib
import sys
from typing import Dict, List, Optional, Tuple

import argcomplete
import pandas as pd

from .entry import Entry, EntryManager, Event, EventType
from .parser import EventParser


def read_events(
    path: pathlib.Path, manager: Optional[EntryManager] = None
) -> EntryManager:
    parser = EventParser()

    if not manager:
        manager = EntryManager()

    with open(path, "r") as f:
        for event in parser.parse(f.readlines()):
            manager.add_event(event)

    return manager


def write_events(path: pathlib.Path, manager: EntryManager) -> None:
    with open(path, "w") as f:
        for e in sorted(manager.get_events()):
            f.write(str(e))
            f.write("\n")


def format_file(path: pathlib.Path) -> None:
    manager = read_events(path)
    write_events(path, manager)


def to_csv(path: pathlib.Path, csv_path: pathlib.Path) -> None:
    manager = read_events(path)
    to_pandas(manager).to_csv(csv_path, index=False)


def to_pandas(manager: EntryManager) -> pd.DataFrame:
    fields, entries = manager.entry_to_tabular()
    return pd.DataFrame(entries, columns=fields)


def server(df: pd.DataFrame):
    from .web import start_server

    start_server(df)


def main():
    parser = argparse.ArgumentParser(description="Event Logger.")
    parser.add_argument("exec", type=str, choices=["view", "format", "csv"])
    parser.add_argument("input", nargs=1, type=pathlib.Path, metavar="PATH")
    parser.add_argument(
        "--output", "-o", nargs=1, default=None, metavar="PATH", type=pathlib.Path
    )
    args = vars(parser.parse_args())

    manager = read_events(args["input"][0])

    if args["exec"] == "view":
        df = to_pandas(manager)
        server(df)
    elif args["exec"] == "format":
        write_events(args["input"][0], manager)
    elif args["exec"] == "csv":
        to_csv(args["input"][0], args["output"][0])


if __name__ == "__main__":
    sys.exit(main())
