from typing import List

import model

class StorageException(Exception):
    pass

class LocalStorage:
    def __init__(self):
        self._id_counter = 0
        self._storage = {}

    def create(self, event: model.Event) -> str:
        for stored_event in self._storage.values():
            if stored_event.date == event.date:
                raise StorageException(f"The event has already been added on the {event.date} date in storage")
        self._id_counter += 1
        event.id = str(self._id_counter)
        self._storage[event.id] = event
        return event.id

    def list(self) -> List[model.Event]:
        return list(self._storage.values())

    def read(self, _id: str) -> model.Event:
        if _id in self._storage:
            raise StorageException(f"{_id} not found in storage")
        return self._storage[_id]

    def update(self, _id: str, event: model.Event):
        if _id not in self._storage:
            raise StorageException(f"{_id} not found in storage")
        event.id = _id
        self._storage[event.id] = event

    def delete(self, _id: str):
        if _id not in self._storage:
            raise StorageException(f"{_id} not found in storage")
        del self._storage[_id]
