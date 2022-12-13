import uuid

from typing import List
from datetime import date, timedelta
from unit.models import Relationship, Address, Phone, FullName, Counterparty, WireCounterparty
from unit.models.account import CreateDepositAccountRequest
from unit.models.application import CreateIndividualApplicationRequest


def create_relationship(_type: str, _id: str, relation: str = None):
    relation = relation or _type
    return {relation: Relationship(_type, _id)}


def create_relationships_dict(relationships: List[Relationship]):
    d = {}

    for r in relationships:
        d.update(r)

    return d


def create_relationship(_type: str, _id: str, relation: str = None):
    relation = relation or _type
    return {relation: Relationship(_type, _id)}

    return d


def create_counterparty_dto(routing_number: str, account_number: str, account_type: str, name: str):
    return Counterparty(routing_number, account_number, account_type, name)


def create_wire_counterparty_dto(routing_number: str, account_number: str, name: str, address: Address):
    return WireCounterparty(routing_number, account_number, name, address)


def generate_uuid():
    return str(uuid.uuid1())


address = Address.from_json_api({
                "street": "5230 Newell Rd",
                "street2": None,
                "city": "Palo Alto",
                "state": "CA",
                "postalCode": "94303",
                "country": "US"
            })

phone = Phone.from_json_api({
                "countryCode": "1",
                "number": "5555555555"
            })

full_name = FullName.from_json_api({
        "first": "Richard",
        "last": "Hendricks"
    })


def create_individual_customer(client):
    request = CreateIndividualApplicationRequest(
        FullName("Jhon", "Doe"), date.today() - timedelta(days=20 * 365),
        Address("1600 Pennsylvania Avenue Northwest", "Washington", "CA", "20500", "US"),
        "jone.doe1@unit-finance.com",
        Phone("1", "2025550108"), ssn="721074426",
    )
    response = client.applications.create(request)
    for key, value in response.data.relationships.items():
        if key == "customer":
            return value.id

    return ""


def create_deposit_account(client):
    customer_id = create_individual_customer(client)
    request = CreateDepositAccountRequest("checking",
                                          {"customer": Relationship("customer", customer_id)},
                                          {"purpose": "credit_operating"})
    return client.accounts.create(request)

