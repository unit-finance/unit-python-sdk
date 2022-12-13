import os
import unittest
from unit import Unit
from unit.models.customer import *
from unit.models.codecs import DtoDecoder
from e2e_tests.helpers.helpers import create_individual_customer

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)

authorized_users = [
    {
        "fullName": {
            "first": "Jared",
            "last": "Dunn"
        },
        "email": "jared@piedpiper.com",
        "phone": {
            "countryCode": "1",
            "number": "1555555590"
        }
    }
]


def get_customer_by_type(type: str):
    response = client.customers.list(ListCustomerParams(0, 1000))
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


def test_business_customer():
    business_customer_api_response = {
        "type": "businessCustomer",
        "id": "1",
        "attributes": {
            "createdAt": "2020-05-10T12:28:37.698Z",
            "name": "Pied Piper",
            "address": {
                "street": "5230 Newell Rd",
                "street2": None,
                "city": "Palo Alto",
                "state": "CA",
                "postalCode": "94303",
                "country": "US"
            },
            "phone": {
                "countryCode": "1",
                "number": "1555555578"
            },
            "stateOfIncorporation": "DE",
            "ein": "123456789",
            "entityType": "Corporation",
            "contact": {
                "fullName": {
                    "first": "Richard",
                    "last": "Hendricks"
                },
                "email": "richard@piedpiper.com",
                "phone": {
                    "countryCode": "1",
                    "number": "1555555578"
                }
            },
            "authorizedUsers": authorized_users,
            "status": "Active",
            "tags": {
                "userId": "106a75e9-de77-4e25-9561-faffe59d7814"
            }
        },
        "relationships": {
            "org": {
                "data": {
                    "type": "org",
                    "id": "1"
                }
            },
            "application": {
                "data": {
                    "type": "businessApplication",
                    "id": "1"
                }
            }
        }
    }

    id = business_customer_api_response["id"]
    _type = business_customer_api_response["type"]

    customer = DtoDecoder.decode(business_customer_api_response)

    assert customer.id == id
    assert customer.type == _type
    assert customer.attributes["address"].street == "5230 Newell Rd"
    assert customer.attributes["name"] == "Pied Piper"
    assert customer.attributes["stateOfIncorporation"] == "DE"
    assert customer.attributes["contact"].full_name.first == "Richard"
    assert customer.attributes["authorizedUsers"][0].full_name.first == "Jared"
    assert customer.attributes["status"] == "Active"


def test_individual_customer():
    individual_customer_api_response = {
        "type": "individualCustomer",
        "id": "8",
        "attributes": {
            "createdAt": "2020-05-12T19:41:04.123Z",
            "fullName": {
                "first": "Peter",
                "last": "Parker"
            },
            "ssn": "721074426",
            "address": {
                "street": "20 Ingram St",
                "street2": None,
                "city": "Forest Hills",
                "state": "NY",
                "postalCode": "11375",
                "country": "US"
            },
            "dateOfBirth": "2001-08-10",
            "email": "peter@oscorp.com",
            "phone": {
                "countryCode": "1",
                "number": "1555555578"
            },
            "authorizedUsers": [],
            "status": "Active",
            "tags": {
                "userId": "106a75e9-de77-4e25-9561-faffe59d7814"
            }
        },
        "relationships": {
            "org": {
                "data": {
                    "type": "org",
                    "id": "1"
                }
            },
            "application": {
                "data": {
                    "type": "individualApplication",
                    "id": "8"
                }
            }
        }
    }

    id = individual_customer_api_response["id"]
    _type = individual_customer_api_response["type"]

    customer = DtoDecoder.decode(individual_customer_api_response)

    assert customer.id == id
    assert customer.type == _type
    assert customer.attributes["address"].street == "20 Ingram St"
    assert customer.attributes["fullName"].first == "Peter"
    assert customer.attributes["fullName"].last == "Parker"
    assert customer.attributes["email"] == "peter@oscorp.com"
    assert customer.attributes["phone"].number == "1555555578"
    assert customer.attributes["authorizedUsers"] == []
    assert customer.attributes["status"] == "Active"


def add_authorized_users_to_individual_customer():
    individual_customer_id = create_individual_customer(client)
    request = AddAuthorizedUsersRequest(individual_customer_id, authorized_users)
    return client.customers.add_authorized_users(request)


def test_add_authorized_users_to_individual_customer():
    response = add_authorized_users_to_individual_customer()
    assert response.data.type == "individualCustomer"
    assert len(response.data.attributes.get("authorizedUsers")) == 1
    assert response.data.attributes.get("authorizedUsers")[0].email == authorized_users[0].get("email")


def test_remove_authorized_users_to_individual_customer():
    add_response = add_authorized_users_to_individual_customer()
    assert add_response.data.type == "individualCustomer"
    assert len(add_response.data.attributes.get("authorizedUsers")) == 1
    assert add_response.data.attributes.get("authorizedUsers")[0].email == authorized_users[0].get("email")
    authorized_users_emails = [authorized_users[0].get("email")]
    request = RemoveAuthorizedUsersRequest(add_response.data.id, authorized_users_emails)
    remove_response = client.customers.remove_authorized_users(request)
    assert remove_response.data.id == add_response.data.id
    assert remove_response.data.type == add_response.data.type
    assert len(remove_response.data.attributes.get("authorizedUsers")) == 0
