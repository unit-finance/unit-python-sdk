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
