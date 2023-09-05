import uuid

from typing import List
from datetime import date, timedelta
from unit.models import Relationship, Address, Phone, FullName, Counterparty, WireCounterparty, Grantor, TrustContact,\
    Trustee, Beneficiary
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


def create_individual_application(client):
    request = CreateIndividualApplicationRequest(
        FullName("Jhon", "Doe"), date.today() - timedelta(days=20 * 365),
        Address("1600 Pennsylvania Avenue Northwest", "Washington", "CA", "20500", "US"),
        "jone.doe1@unit-finance.com",
        Phone("1", "2025550108"), ssn="721074426",
        occupation="ArchitectOrEngineer"
    )
    return client.applications.create(request)


def create_individual_customer(client):
    response = create_individual_application(client)

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


def create_grantor():
    return Grantor.from_json_api({
                                                "fullName": {
                                                    "first": "Laurie",
                                                    "last": "Bream"
                                                },
                                                "dateOfBirth": "2000-01-01",
                                                "ssn": "000000003",
                                                "email": "laurie@raviga.com",
                                                "phone": {
                                                    "countryCode": "1",
                                                    "number": "2025550108"
                                                },
                                                "address": {
                                                    "street": "950 Allerton Street",
                                                    "city": "Redwood City",
                                                    "state": "CA",
                                                    "postalCode": "94063",
                                                    "country": "US"
                                                }
                                            })


def create_trust_contact():
    return TrustContact.from_json_api({
        "fullName": {
          "first": "Jared",
          "last": "Dunn"
        },
        "email": "jared@piedpiper.com",
        "phone": {
          "countryCode": "1",
          "number": "2025550108"
        },
        "address": {
          "street": "5230 Newell Rd",
          "city": "Palo Alto",
          "state": "CA",
          "postalCode": "94303",
          "country": "US"
        }
      })


def create_trustee():
    return [Trustee.from_json_api({
          "fullName": {
            "first": "Richard",
            "last": "Hendricks"
          },
          "dateOfBirth": "2000-01-01",
          "ssn": "000000002",
          "email": "richard@piedpiper.com",
          "phone": {
            "countryCode": "1",
            "number": "2025550108"
          },
          "address": {
            "street": "5230 Newell Rd",
            "city": "Palo Alto",
            "state": "CA",
            "postalCode": "94303",
            "country": "US"
          }
        })]


def create_beneficiaries():
    return [
        Beneficiary.from_json_api({
          "fullName": {
            "first": "Dinesh",
            "last": "Chugtai"
          },
          "dateOfBirth": "2000-01-01"
        }),
        Beneficiary.from_json_api({
          "fullName": {
            "first": "Gilfoyle",
            "last": "Unknown"
          },
          "dateOfBirth": "2000-01-01"
        })
    ]
