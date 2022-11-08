import os
import unittest
import pytest

from unit import Unit
from unit.models.account import *
from e2e_tests.helpers.helpers import create_deposit_account, close_credit_account, create_individual_customer,\
    create_deposit_account_for_business, create_credit_account_for_business

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)


@pytest.fixture
def credit_account():
    return create_credit_account_for_business(client).data


@pytest.fixture
def deposit_account():
    return create_deposit_account(client).data


@pytest.fixture()
def account_with_owners(deposit_account):
    account_id = deposit_account.id
    customer_ids = [create_individual_customer(client), create_individual_customer(client)]
    return client.accounts.add_owners(AccountOwnersRequest(account_id,
                                                           RelationshipArray.from_ids_array("customer",
                                                                                            customer_ids))).data


def test_create_deposit_account(deposit_account):
    assert deposit_account.type == "depositAccount"


def test_create_credit_account_for_business(credit_account):
    assert credit_account
    assert credit_account.type == "creditAccount"
    res = close_credit_account(client, credit_account.id)
    assert res.data.attributes.get("status").__eq__("Closed")


def test_create_deposit_account_for_business():
    account = create_deposit_account_for_business(client).data
    assert account.type == "depositAccount"


def test_create_joint_deposit_account():
    customer_id1 = create_individual_customer(client)
    customer_id2 = create_individual_customer(client)
    request = CreateDepositAccountRequest("checking",
                                          {"customers": RelationshipArray([
                                            Relationship("customer", customer_id1),
                                            Relationship("customer", customer_id2)])},
                                          {"purpose": "checking"})
    response = client.accounts.create(request)
    assert response.data.type == "depositAccount"


def test_get_deposit_account(deposit_account):
    account_id = deposit_account.id
    response = client.accounts.get(account_id, "customer")
    assert response.data.type == "depositAccount" and isinstance(response.included, list)


def test_list_accounts():
    response = client.accounts.list()
    for acc in response.data:
        assert acc.type == "depositAccount"


def test_list_credit_accounts(credit_account):
    assert credit_account

    response = client.accounts.list(ListAccountParams(_type="credit"))
    assert response.data is not None
    for acc in response.data:
        assert acc.type == "creditAccount"

    accounts_to_close = list(filter(lambda x: x.attributes.get("status").__eq__("Open"), response.data))
    for acc in accounts_to_close:
        res = close_credit_account(client, acc.id)
        assert res.data.attributes.get("status").__eq__("Closed")


def test_limits_account(deposit_account):
    account_id = deposit_account.id
    response = client.accounts.limits(account_id)
    assert response.data.type == "limits"


def test_close_account(deposit_account):
    account_id = deposit_account.id
    request = CloseDepositAccountRequest(account_id, "Fraud")
    response = client.accounts.close_account(request)
    assert response.data.type == "depositAccount"


def test_close_and_reopen_account(deposit_account):
    account_id = deposit_account.id
    request = CloseDepositAccountRequest(account_id)
    response = client.accounts.close_account(request)
    assert response.data.type == "depositAccount"
    response = client.accounts.reopen_account(account_id)
    assert response.data.type == "depositAccount"


def test_update_account(deposit_account):
    account_id = deposit_account.id
    request = PatchDepositAccountRequest(account_id, tags={
        "purpose": "tax",
        "trackUserId": "userId_fe6885b5815463b26f65e71095832bdd916890f7"})
    response = client.accounts.update(request)
    assert response.data.type == "depositAccount"
    assert response.data.attributes.get("tags").get("purpose") == "tax"


def test_update_credit_account(credit_account):
    account_id = credit_account.id
    _credit_limit = 40000
    request = PatchCreditAccountRequest(account_id, tags={
        "purpose": "tax",
        "trackUserId": "userId_fe6885b5815463b26f65e71095832bdd916890f7"},
                                        credit_limit=_credit_limit)
    response = client.accounts.update(request)
    assert response.data.type == "creditAccount"
    assert response.data.attributes.get("creditLimit") == _credit_limit
    assert response.data.attributes.get("tags").get("purpose") == "tax"


def test_get_deposit_products(deposit_account):
    assert deposit_account.type == "depositAccount"

    response = client.accounts.list()
    assert len(response.data) > 0

    for acc in response.data:
        deposit_products = client.accounts.get_deposit_products(acc.id).data
        for dp in deposit_products:
            assert dp.type == "accountDepositProduct"


def test_add_owners(account_with_owners):
    assert account_with_owners.type == "depositAccount"
    assert account_with_owners.relationships["customers"].data is not None
    assert len(account_with_owners.relationships["customers"].data) == 3


def test_remove_owners(account_with_owners):
    assert account_with_owners.type == "depositAccount"
    account_id = account_with_owners.id

    # Account should have at least one owner
    last_owner_id = account_with_owners.relationships["customers"].data.pop().id
    response = client.accounts.remove_owners(AccountOwnersRequest(account_id,
                                                                  account_with_owners.relationships["customers"]))
    assert response.data.type == "depositAccount"
    assert response.data.relationships.get("customer").id == last_owner_id
