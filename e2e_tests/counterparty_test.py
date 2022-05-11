import os
import unittest
from unit import Unit
from unit.models.counterparty import *
from e2e_tests.account_test import create_individual_customer

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)

def create_counterparty():
    customer_id = create_individual_customer()
    request = CreateCounterpartyRequest("Joe Doe", "123456789", "123", "Checking", "Person",
                                        {"customer": Relationship("customer", customer_id)})
    return client.counterparty.create(request)

def test_create_counterparty():
    response = create_counterparty()
    assert response.data.type == "achCounterparty"

def test_delete_counterparty():
    counterparty_id = create_counterparty().data.id
    response = client.counterparty.delete(counterparty_id)
    assert response.data == []

def test_get_counterparty():
    counterparty_id = create_counterparty().data.id
    response = client.counterparty.get(counterparty_id)
    assert response.data.type == "achCounterparty"


def test_counterparty_list():
    response = client.counterparty.list()
    for c in response.data:
        assert c.type == "achCounterparty"


def test_create_couterparty():
    create_counterparty_json = {
        "data": {
            "type": "achCounterparty",
            "attributes": {
                "name": "Joe Doe",
                "routingNumber": "011000133",
                "accountNumber": "123",
                "accountType": "Checking",
                "type": "Person",
                "tags": {"purpose": "testing_creation"}
            },
            "relationships": {
                "customer": {
                    "data": {
                        "type": "customer",
                        "id": "111111"
                    }
                }
            }
        }
    }

    create_counterparty_object = CreateCounterpartyRequest("Joe Doe", "011000133", "123", "Checking", "Person",
                                                           {"customer": Relationship("customer", "111111")},
                                                           {"purpose": "testing_creation"})
    payload = create_counterparty_object.to_json_api()

    assert payload["data"]["attributes"]["name"] == create_counterparty_json["data"]["attributes"]["name"]
    assert payload["data"]["attributes"]["routingNumber"] == create_counterparty_json["data"]["attributes"]["routingNumber"]
    assert payload["data"]["attributes"]["accountNumber"] == create_counterparty_json["data"]["attributes"]["accountNumber"]
    assert payload["data"]["attributes"]["accountType"] == create_counterparty_json["data"]["attributes"]["accountType"]
    assert payload["data"]["attributes"]["type"] == create_counterparty_json["data"]["attributes"]["type"]
    assert payload["data"]["type"] == create_counterparty_json["data"]["type"]


def test_create_with_token_couterparty():
    create_counterparty_json = {
         "data": {
            "type": "achCounterparty",
            "attributes": {
              "name": "Sherlock Holmes",
              "plaidProcessorToken": "processor-5a62q307-ww0a-6737-f6db-pole26004556",
              "type": "Person",
              "permissions": "DebitOnly",
              "tags": {"purpose": "testing_creation"}
            },
            "relationships": {
              "customer": {
                "data": {
                  "type": "customer",
                  "id": "111111"
                }
              }
            }
         }
    }

    create_counterparty_object = CreateCounterpartyWithTokenRequest("Sherlock Holmes", "Person",
                                                                    "processor-5a62q307-ww0a-6737-f6db-pole26004556",
                                                                    {"customer": Relationship("customer", "111111")},
                                                                    permissions="DebitOnly",
                                                                    tags={"purpose": "testing_creation"}
                                                                    )
    payload = create_counterparty_object.to_json_api()

    assert payload["data"]["type"] == create_counterparty_json["data"]["type"]
    assert payload["data"]["attributes"]["type"] == create_counterparty_json["data"]["attributes"]["type"]
    assert payload["data"]["attributes"]["name"] == create_counterparty_json["data"]["attributes"]["name"]
    assert payload["data"]["attributes"]["plaidProcessorToken"] == create_counterparty_json["data"]["attributes"]["plaidProcessorToken"]
    assert payload["data"]["attributes"]["permissions"] == create_counterparty_json["data"]["attributes"]["permissions"]
    assert payload["data"]["attributes"]["tags"] == create_counterparty_json["data"]["attributes"]["tags"]

def test_counterparty_dto():
    counterparty_api_response = {
          "type": "achCounterparty",
          "id": "8",
          "attributes": {
            "createdAt": "2020-05-13T09:07:47.645Z",
            "name": "Joe Doe",
            "routingNumber": "011000138",
            "bank": "Bank Of America",
            "accountNumber": "123",
            "accountType": "Checking",
            "type": "Person",
            "permissions": "CreditOnly"
          },
          "relationships": {
            "customer": {
              "data": {
                "type": "customer",
                "id": "111111"
              }
            }
          }
    }

    id = counterparty_api_response["id"]
    attributes = counterparty_api_response["attributes"]
    relationships = counterparty_api_response["relationships"]
    _type = counterparty_api_response["type"]

    counterparty = CounterpartyDTO.from_json_api(id, _type, attributes, relationships)

    assert counterparty.id == id
    assert counterparty.attributes["bank"] == counterparty_api_response["attributes"]["bank"]
    assert counterparty.attributes["accountNumber"] == counterparty_api_response["attributes"]["accountNumber"]
    assert counterparty.attributes["routingNumber"] == counterparty_api_response["attributes"]["routingNumber"]
    assert counterparty.attributes["accountType"] == counterparty_api_response["attributes"]["accountType"]
    assert counterparty.attributes["permissions"] == counterparty_api_response["attributes"]["permissions"]
    assert counterparty.attributes["type"] == counterparty_api_response["attributes"]["type"]
    assert counterparty.attributes["name"] == counterparty_api_response["attributes"]["name"]
