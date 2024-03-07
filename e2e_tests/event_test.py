import os
import pytest
from datetime import datetime, date, timedelta
from unit import Unit
from unit.models.codecs import DtoDecoder
from unit.models.event import TaxFormCreatedEvent, TaxFormUpdatedEvent

token = os.environ.get("TOKEN")
client = Unit("https://api.s.unit.sh", token)


def test_list_and_get_events():
    response = client.events.list()
    for e in response.data:
        assert "." in e.type
        event = client.events.get(e.id).data
        assert "." in event.type
        assert e.type == event.type
        assert e.id == event.id


def test_fire_event():
    event_id = client.events.list().data[0].id
    response = client.events.fire(event_id)
    assert response.data == []


def test_tax_form_created_event():
    payload = {
          "id": "1",
          "type": "taxForm.created",
          "attributes": {
            "createdAt": "2021-11-29T17:23:08.778Z",
            "taxYear": "2023",
            "formType": "1099-INT",
            "revision": 0
          },
          "relationships": {
            "taxForm": {
              "data": {
                "id": "18",
                "type": "taxForm"
              }
            },
            "customer": {
              "data": {
                "id": "10000",
                "type": "customer"
              }
            }
          }
        }

    event = DtoDecoder.decode(payload)
    assert type(event) is TaxFormCreatedEvent
    assert event.attributes.get("taxYear") == payload.get("attributes").get("taxYear")


def test_tax_form_updated_event():
    payload = {
                "id": "1",
                "type": "taxForm.updated",
                "attributes": {
                    "createdAt": "2021-11-29T17:23:08.778Z",
                    "taxYear": "2023",
                    "formType": "1099-INT",
                    "revision": 1
                },
                "relationships": {
                    "taxForm": {
                        "data": {
                            "id": "18",
                            "type": "taxForm"
                        }
                    },
                    "customer": {
                        "data": {
                            "id": "10000",
                            "type": "customer"
                        }
                    }
                }
            }

    event = DtoDecoder.decode(payload)
    assert type(event) is TaxFormUpdatedEvent
    assert event.attributes.get("taxYear") == payload.get("attributes").get("taxYear")
