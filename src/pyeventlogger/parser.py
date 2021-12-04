import re
from dataclasses import dataclass
from datetime import date, datetime, time
from typing import Dict, Iterable, Iterator, List, Optional, Tuple

from .entry import Event, EventType


@dataclass
class ParserEvent:
    """"""

    date: str
    time: Optional[str]
    type: str
    entry_id: str
    title: str


class EventFactory:
    """"""

    token_to_type = {
        "!": EventType.EVENT,
        "new": EventType.NEW,
    }

    def from_parser_event(self, parser_event: ParserEvent) -> Event:
        """"""

        e_date = datetime.strptime(parser_event.date, "%Y-%m-%d").date()
        e_time = None
        if parser_event.time:
            e_time = datetime.strptime(parser_event.time, "%H:%M:%S").time()
        e_type = self.token_to_type[parser_event.type]
        if parser_event.entry_id is None:
            raise ValueError("No entry ID")
        e_title = parser_event.title or ""

        return Event(
            date=e_date,
            time=e_time,
            type=e_type,
            entry_id=parser_event.entry_id,
            title=e_title,
            metadata={},
        )


class ParserError(Exception):
    """"""

    def __init__(self, idx, line):
        super().__init__(f"Parser error at line {idx} : {line}")


class EventParser:
    """"""

    pattern_date = re.compile(r"\d\d\d\d-\d\d-\d\d")
    pattern_time = re.compile(r"\d\d:\d\d:\d\d")
    pattern_new = re.compile(r"new")
    pattern_id = re.compile(r"[A-Za-z\-_0-9]*")
    pattern_update = re.compile(r"!")
    pattern_field = re.compile(r"\"((?:\\.|[^\"])*)\"")
    pattern_tab = re.compile(r"\t")
    pattern_sep = re.compile(r":")
    pattern_metadata = re.compile(r'\s*"((?:\\.|[^"])*)"\s*:\s*"((?:\\.|[^"])*)"')

    pattern_event = re.compile(
        r"""^\s*(\d{4}-\d{2}-\d{2})\s+(?:(\d{2}:\d{2}:\d{2})?|\s)\s*(!|new)\s+([\d\w\-_\.]+)(?:\s+\"((?:\\.|[^\"])*)\")?$""",
        re.UNICODE,
    )

    factory = EventFactory()

    def parse(self, content: Iterable[str]) -> Iterator[Event]:
        """"""
        prev_event: Optional[Event] = None
        for idx, line in enumerate(content):
            line = line.rstrip()

            if line == "":
                continue

            event = self._parse_event(line)

            if event:
                prev_event = event
                event = None

                if prev_event is not None:
                    yield prev_event

                continue

            if event is None and prev_event is not None:
                metadata = self._parse_metadata(line)

                if metadata is None:
                    continue

                prev_event.metadata[metadata[0]] = metadata[1]
                continue

            raise ParserError(idx, line)

        return event

    def _parse_event(self, current_content: str) -> Optional[Event]:
        """"""
        m = self.pattern_event.match(current_content)

        if m is None:
            return None

        event = self.factory.from_parser_event(
            ParserEvent(
                date=m.group(1),
                time=m.group(2),
                type=m.group(3),
                entry_id=m.group(4),
                title=m.group(5),
            )
        )

        return event

    def _parse_metadata(self, line: str) -> Optional[Tuple[str, str]]:
        """"""
        m = self.pattern_metadata.match(line)

        if m is None:
            return None

        return (m.group(1), m.group(2))
