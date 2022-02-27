import os
import unittest
from unit import Unit
from unit.models.customer import *

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)

def get_customer_by_type(type: str):
    response = client.customers.list(ListCustomerParams(0,1000))
    for c in response.data:
        if c.type == type:
            return c
    return None

def test_update_individual_customer():
    individual_customer_id = get_customer_by_type("individualCustomer").id
    request = PatchIndividualCustomerRequest(individual_customer_id, phone=Phone("1", "1115551111"))
    response = client.customers.update(request)
    assert response.data.type == "individualCustomer"

def test_update_business_customer():
    business_customer_id = get_customer_by_type("businessCustomer").id
    request = PatchBusinessCustomerRequest(business_customer_id, phone=Phone("1", "1115551111"))
    response = client.customers.update(request)
    assert response.data.type == "businessCustomer"

def test_get_customer():
    customer_ids = []
    response = client.customers.list()
    for c in response.data:
        customer_ids.append(c.id)

    for id in customer_ids:
        response = client.customers.get(id)
        assert response.data.type == "individualCustomer" or response.data.type == "businessCustomer"

def test_list_customers():
    response = client.customers.list()
    for customer in response.data:
        assert customer.type == "individualCustomer" or customer.type == "businessCustomer"
