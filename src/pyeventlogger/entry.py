""""""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time
from enum import Enum
from functools import total_ordering
from typing import Dict, Iterator, List, Optional, Tuple

from sortedcontainers.sortedlist import SortedList


class EventType(Enum):
    """"""

    EVENT = 1
    NEW = 2

    def __str__(self):
        if self == EventType.EVENT:
            return "!"
        elif self == EventType.NEW:
            return "new"

        raise Exception()


@dataclass
@total_ordering
class Event:
    """"""

    date: date
    time: Optional[time]
    entry_id: str
    type: EventType
    title: Optional[str]
    metadata: Dict[str, str]

    def __str__(self):
        lines = []
        first = []

        first.append(self.date.strftime("%Y-%m-%d"))

        if self.time:
            first.append(self.time.strftime("%H:%M:%S"))

        first.append(self.type.__str__())
        first.append(self.entry_id)
        if self.title:
            first.append(f'"{self.title}"')

        lines.append(" ".join(first))

        for k, v in self.metadata.items():
            lines.append(f'\t"{k}": "{v}"')

        return "\n".join(lines)

    def __lt__(self, other: Event) -> bool:
        return datetime.combine(
            self.date, self.time or datetime.min.time()
        ) < datetime.combine(other.date, other.time or datetime.min.time())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Event):
            return NotImplemented

        return datetime.combine(
            self.date, self.time or datetime.min.time()
        ) == datetime.combine(other.date, other.time or datetime.min.time())


class Entry(SortedList[Event]):
    """"""

    def add_event(self, event: Event) -> None:
        self.events.append(event)

    def get_metadata(self, idx: Optional[int] = None) -> Dict[str, str]:
        metadata = None

        for metadata in self.gen_metadata(idx, copy=False):
            pass

        return metadata or {}

    def gen_metadata(
        self, idx: Optional[int] = None, copy: bool = True
    ) -> Iterator[Dict[str, str]]:
        if not idx:
            idx = self.__len__()

        metadata: Dict[str, str] = {}

        for event in self[:idx]:
            for k, v in event.metadata.items():
                metadata[k] = v

            if copy:
                yield metadata.copy()
            else:
                yield metadata

        return

    def append(self, value):
        self.add(value)

    def insert(self, index, value):
        self.add(value)

    def extend(self, values):
        self.update(values)

    def reverse(self):
        raise NotImplementedError()

    def get_creation_date_time(self) -> Tuple[date, Optional[time]]:
        return self[0].date, self[0].time

    def get_last_changed_date_time(self) -> Tuple[date, Optional[time]]:
        return self[-1].date, self[-1].time

    def __lt__(self, other: Entry):
        return self[-1] == other[-1] and self[0] < other[0] or self[-1] < other[-1]


class EntryManager:
    """"""

    def __init__(self):
        self.entries: Dict[str, Entry] = {}

    def add_event(self, event: Event):
        """"""
        if event.entry_id not in self.entries:
            self.entries[event.entry_id] = Entry()

        self.entries[event.entry_id].append(event)

    def get_events(self) -> List[Event]:
        events: List[Event] = []

        for entry in self.entries.values():
            for event in entry:
                events.append(event)

        return sorted(events)

    def get_metadata_fields(self) -> List[str]:
        fields = set()

        for entry in self.entries.values():
            for event in entry:
                for field in event.metadata:
                    fields.add(field)

        return list(fields)

    def entry_to_tabular(self) -> Tuple[List[str], List[List[str]]]:
        fields = [
            "creation date",
            "creation time",
            "last changed date",
            "last changed time",
            "id",
        ] + self.get_metadata_fields()
        field_idx: Dict[str, int] = {}
        field_number = len(fields)

        for i, f in enumerate(fields):
            field_idx[f] = i

        tab: List[List[str]] = []

        for entry_id, entry in sorted(list(self.entries.items()), key=lambda x: x[1]):
            line: List[str] = [""] * field_number

            for k, v in entry.get_metadata().items():
                line[field_idx[k]] = v

            c_date, c_time = entry.get_creation_date_time()
            l_date, l_time = entry.get_last_changed_date_time()

            line[field_idx["creation date"]] = c_date.strftime("%Y-%m-%d")
            line[field_idx["last changed date"]] = l_date.strftime("%Y-%m-%d")

            if c_time:
                line[field_idx["creation time"]] = c_time.strftime("%H-%M-%S")
            if l_time:
                line[field_idx["last changed time"]] = l_time.strftime("%H-%M-%S")

            line[field_idx["id"]] = entry_id

            tab.append(line)

        return fields, tab
