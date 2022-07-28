import os
import pytest
from datetime import datetime, date, timedelta
from unit import Unit

token = os.environ.get("TOKEN")
client = Unit("https://api.s.unit.sh", token)

def test_list_and_get_events():
    event_ids = []
    response = client.events.list()
    for e in response.data:
        assert "." in e.type
        event_ids.append(e.id)

    for e in event_ids:
        response = client.events.get(e)
        assert "." in response.data.type

def test_fire_event():
    event_id = client.events.list().data[0].id
    response = client.events.fire(event_id)
    assert response.data == []

