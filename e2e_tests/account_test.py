import os
import unittest
from datetime import timedelta
from unit import Unit
from unit.models.account import *
from unit.models.application import CreateIndividualApplicationRequest

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)


def create_individual_customer():
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


def create_deposit_account():
    customer_id = create_individual_customer()
    request = CreateDepositAccountRequest("checking",
                                          {"customer": Relationship("customer", customer_id)},
                                          {"purpose": "checking"})
    return client.accounts.create(request)


def test_create_deposit_account():
    response = create_deposit_account()
    assert response.data.type == "depositAccount"


def test_create_joint_deposit_account():
    customer_id1 = create_individual_customer()
    customer_id2 = create_individual_customer()
    request = CreateDepositAccountRequest("checking",
                                          {"customers": RelationshipArray([
                                            Relationship("customer", customer_id1),
                                            Relationship("customer", customer_id2)])},
                                          {"purpose": "checking"})
    response = client.accounts.create(request)
    assert response.data.type == "depositAccount"


def test_get_account():
    account_id = create_deposit_account().data.id
    response = client.accounts.get(account_id, "customer")
    assert response.data.type == "depositAccount" and isinstance(response.included, list)


def test_list_accounts():
    response = client.accounts.list()
    for acc in response.data:
        assert acc.type == "depositAccount"


def test_limits_account():
    account_id = create_deposit_account().data.id
    response = client.accounts.limits(account_id)
    assert response.data.type == "limits"


def test_close_and_reopen_account():
    account_id = create_deposit_account().data.id
    requet = CloseAccountRequest(account_id, "Fraud")
    response = client.accounts.close_account(requet)
    assert response.data.type == "depositAccount"
    account_id = create_deposit_account().data.id
    requet = CloseAccountRequest(account_id)
    response = client.accounts.close_account(requet)
    assert response.data.type == "depositAccount"
    response = client.accounts.reopen_account(account_id)
    assert response.data.type == "depositAccount"


def test_update_account():
    account_id = create_deposit_account().data.id
    request = PatchDepositAccountRequest(account_id, tags={
        "purpose": "tax",
        "trackUserId": "userId_fe6885b5815463b26f65e71095832bdd916890f7"})
    response = client.accounts.update(request)
    assert response.data.type == "depositAccount"

