import os
import pathlib
import sys
from typing import Iterable, Iterator

import pytest
from src.parser import EventParser

assets_path = pathlib.Path(__file__).parent.absolute().joinpath("assets")
src_path = pathlib.Path(__file__).parent.parent.absolute().joinpath("src")


@pytest.fixture
def my_parser() -> EventParser:
    """"""
    return EventParser()


@pytest.fixture
def simple_entry() -> Iterable[str]:
    """"""
    string = ""

    with open(assets_path.joinpath("simple_entry.txt"), "r") as file:
        return file.readlines()

    return


def test_parse(my_parser: EventParser, simple_entry: Iterable[str]):
    """"""
    print(simple_entry)
    event_list = list(my_parser.parse(simple_entry))
    print(event_list)

    assert len(event_list) > 0
