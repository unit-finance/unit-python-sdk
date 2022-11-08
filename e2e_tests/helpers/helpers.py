import uuid
from datetime import date, timedelta

from unit.models import Relationship, Address, Phone, FullName, BusinessContact, Officer, BeneficialOwner
from unit.models.account import CreateDepositAccountRequest, CloseCreditAccountRequest, CreateCreditAccountRequest
from unit.models.application import CreateIndividualApplicationRequest, CreateBusinessApplicationRequest


def create_relationship(_type: str, _id: str, relation: str = None):
    relation = relation or _type
    return {relation: Relationship(_type, _id)}


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


def create_business_application(client):
    request = CreateBusinessApplicationRequest(
        name="Acme Inc.",
        address=Address("1600 Pennsylvania Avenue Northwest", "Washington", "CA", "20500", "US"),
        phone=Phone("1", "9294723497"), state_of_incorporation="CA", entity_type="Corporation", ein="123456789",
        officer=Officer(full_name=FullName("Jone", "Doe"), date_of_birth=date.today() - timedelta(days=20 * 365),
                        address=Address("950 Allerton Street", "Redwood City", "CA", "94063", "US"),
                        phone=Phone("1", "2025550108"), email="jone.doe@unit-finance.com", ssn="123456789"),
        contact=BusinessContact(full_name=FullName("Jone", "Doe"), email="jone.doe@unit-finance.com",
                                phone=Phone("1", "2025550108")),
        beneficial_owners=[
            BeneficialOwner(
                FullName("James", "Smith"), date.today() - timedelta(days=20*365),
                Address("650 Allerton Street","Redwood City","CA","94063","US"),
                Phone("1","2025550127"),"james@unit-finance.com",ssn="574567625"),
            BeneficialOwner(FullName("Richard","Hendricks"), date.today() - timedelta(days=20 * 365),
                            Address("470 Allerton Street", "Redwood City", "CA", "94063", "US"),
                            Phone("1", "2025550158"), "richard@unit-finance.com", ssn="574572795")
        ]
    )

    return client.applications.create(request)


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


def create_deposit_account_for_business(client):
    customer_id = create_business_customer(client)

    request = CreateDepositAccountRequest("checking",
                                          {"customer": Relationship("customer", customer_id)},
                                          {"purpose": "checking"})
    return client.accounts.create(request)


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


def create_business_customer(client):
    b_app = create_business_application(client).data
    return b_app.relationships.get("customer").id


def create_deposit_account(client):
    customer_id = create_individual_customer(client)
    request = CreateDepositAccountRequest("checking",
                                          {"customer": Relationship("customer", customer_id)},
                                          {"purpose": "checking"})
    return client.accounts.create(request)


def create_credit_account_for_business(client):
    customer_id = create_business_customer(client)
    request = CreateCreditAccountRequest("credit_terms_test", 20000, create_relationship("customer", customer_id),
                                         {"purpose": "some_purpose"})
    return client.accounts.create(request)


def close_credit_account(client, account_id):
    return client.accounts.close_account(CloseCreditAccountRequest(account_id))
