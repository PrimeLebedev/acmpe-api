from datetime import date

from flask import Flask
from flask import request


app = Flask(__name__)

API_ROOT = '/api/v1'
CALENDAR_API_ROOT = API_ROOT + '/calendar'

import model
import logic

_event_logic = logic.EventLogic()

class ApiException(Exception):
    pass

def _from_raw(raw_event: str) -> model.Event:
    parts = raw_event.split('|')
    event = model.Event()
    if len(parts) == 3:
        part_date = parts[0].split(',')
        event.id = None
        event.date = date(int(part_date[0]), int(part_date[1]), int(part_date[2]))
        event.title = parts[1]
        event.text = parts[2]
        return event
    else:
        raise ApiException(f"invalid RAW event data {raw_event}")


def _to_raw(event: model.Event) -> str:
    return f"{event.date}|{event.title}|{event.text}"


@app.route(CALENDAR_API_ROOT + "/", methods=["POST"])
def create():
    try:
        data = request.get_data().decode('utf-8')
        event = _from_raw(data)
        _id = _event_logic.create(event)
        return f"new id: {_id}", 201
    except Exception as ex:
        return f"failed to CREATE with: {ex}", 404


@app.route(CALENDAR_API_ROOT + "/", methods=["GET"])
def list():
    try:
        events = _event_logic.list()
        raw_events = ""
        for event in events:
            raw_events += _to_raw(event) + '\n'
        return raw_events, 200
    except Exception as ex:
        return f"failed to LIST with: {ex}", 404


@app.route(CALENDAR_API_ROOT + "/<_id>/", methods=["GET"])
def read(_id: str):
    try:
        event = _event_logic.read(_id)
        raw_event = _to_raw(event)
        return raw_event, 200
    except Exception as ex:
        return f"failed to READ with: {ex}", 404


@app.route(CALENDAR_API_ROOT + "/<_id>/", methods=["PUT"])
def update(_id: str):
    try:
        data = request.get_data().decode('utf-8')
        event = _from_raw(data)
        _event_logic.update(_id, event)
        return "updated", 200
    except Exception as ex:
        return f"failed to UPDATE with: {ex}", 404


@app.route(CALENDAR_API_ROOT + "/<_id>/", methods=["DELETE"])
def delete(_id: str):
    try:
        _event_logic.delete(_id)
        return "deleted", 200
    except Exception as ex:
        return f"failed to DELETE with: {ex}", 404
