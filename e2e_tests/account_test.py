import os
import unittest
from datetime import timedelta

from e2e_tests.application_test import create_business_application
from unit import Unit
from unit.models.account import *
from unit.models.application import CreateIndividualApplicationRequest
from e2e_tests.helpers.helpers import create_relationship

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


def create_business_customer():
    b_app = create_business_application().data
    return b_app.relationships.get("customer").id


def create_deposit_account():
    customer_id = create_individual_customer()
    request = CreateDepositAccountRequest("checking",
                                          {"customer": Relationship("customer", customer_id)},
                                          {"purpose": "checking"})
    return client.accounts.create(request)


def test_create_deposit_account():
    response = create_deposit_account()
    assert response.data.type == "depositAccount"


def create_deposit_account_for_business():
    customer_id = create_business_customer()

    request = CreateDepositAccountRequest("checking",
                                          {"customer": Relationship("customer", customer_id)},
                                          {"purpose": "checking"})
    return client.accounts.create(request)


def create_credit_account_for_business():
    customer_id = create_business_customer()
    request = CreateCreditAccountRequest("credit_terms_test", 20000, create_relationship("customer", customer_id),
                                         {"purpose": "some_purpose"})
    return client.accounts.create(request)


def test_create_credit_account_for_business():
    response = create_credit_account_for_business()
    assert response.data.type == "creditAccount"


def test_create_deposit_account_for_business():
    response = create_deposit_account_for_business()
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


def test_close_account():
    account_id = create_deposit_account().data.id
    requet = CloseAccountRequest(account_id, "Fraud")
    response = client.accounts.close_account(requet)
    assert response.data.type == "depositAccount"


def test_close_and_reopen_account():
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
    assert response.data.attributes.get("tags").get("purpose") == "tax"


def test_update_credit_account():
    account_id = create_credit_account_for_business().data.id
    _credit_limit = 4000
    request = PatchCreditAccountRequest(account_id, tags={
        "purpose": "tax",
        "trackUserId": "userId_fe6885b5815463b26f65e71095832bdd916890f7"},
                                        credit_limit=_credit_limit)
    response = client.accounts.update(request)
    assert response.data.type == "creditAccount"
    assert response.data.attributes.get("creditLimit") == _credit_limit
    assert response.data.attributes.get("tags").get("purpose") == "tax"


def test_get_deposit_products():
    response = create_deposit_account()
    assert response.data.type == "depositAccount"
    response = client.accounts.list()
    assert len(response.data) > 0

    for acc in response.data:
        deposit_products = client.accounts.get_deposit_products(acc.id).data
        for dp in deposit_products:
            assert dp.type == "accountDepositProduct"


def add_owners():
    account_id = create_deposit_account().data.id
    customer_ids = [create_individual_customer(), create_individual_customer()]
    return client.accounts.add_owners(AccountOwnersRequest(account_id,
                                                           RelationshipArray.from_ids_array("customer",
                                                                                            customer_ids)))


def test_add_owners():
    response = add_owners()
    assert response.data.type == "depositAccount"
    assert response.data.relationships["customers"].data is not None
    assert len(response.data.relationships["customers"].data) == 3


def test_remove_owners():
    response = add_owners()
    assert response.data.type == "depositAccount"
    account_id = response.data.id
    last_owner_id = response.data.relationships["customers"].data.pop().id # An account should have at least one owner
    response = client.accounts.remove_owners(AccountOwnersRequest(account_id, response.data.relationships["customers"]))
    assert response.data.type == "depositAccount"
    assert response.data.relationships.get("customer").id == last_owner_id
