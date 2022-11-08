import os
import unittest

import pytest
import requests

from e2e_tests.account_test import create_credit_account_for_business
from unit import Unit
from unit.models.card import CreateIndividualDebitCard, PatchIndividualDebitCard, ListCardParams, \
    CreateBusinessDebitCard, CreateBusinessVirtualDebitCard, CreateBusinessCreditCard, CreateBusinessVirtualCreditCard, \
    PatchBusinessDebitCard, PatchBusinessCreditCard
from unit.models.account import *
from e2e_tests.helpers.helpers import create_relationship, generate_uuid, full_name, address, phone, \
    create_deposit_account, create_deposit_account_for_business

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)

card_types = ["individualDebitCard", "businessDebitCard", "individualVirtualDebitCard", "businessVirtualDebitCard"]

headers = {
            "content-type": "application/vnd.api+json",
            "authorization": f"Bearer {token}",
            "user-agent": "unit-python-sdk"
        }


def create_individual_debit_card():
    account_id = create_deposit_account(client).data.id
    request = CreateIndividualDebitCard(relationships={
        "account": {
            "data": {
                "type": "depositAccount",
                "id": account_id
            }
        }
    })
    response = client.cards.create(request)
    res = requests.post(f"https://api.s.unit.sh/sandbox/cards/{response.data.id}/activate/", headers=headers)

    if res.status_code != 200:
        print("Failed to activate card")

    return response


@pytest.fixture()
def individual_debit_card():
    return create_individual_debit_card().data


def find_card_id(criteria: Dict[str, str]):
    def filter_func(card):
        for key, value in criteria.items():
            if key not in card.attributes:
                if getattr(card, key) != value:
                    return False
            elif card.attributes[key] != value:
                return False
        return True

    response = client.cards.list(ListCardParams(0,1000))
    filtered = list(filter(filter_func, response.data))

    if len(filtered) > 0:
        return filtered[0].id
    else:
        response = create_individual_debit_card()
        return response.data.id


@pytest.fixture()
def business_debit_card():
    account_id = create_deposit_account_for_business(client).data.id

    request = CreateBusinessDebitCard(full_name, "2001-08-10", address, phone, "richard@piedpiper.com",
                                      shipping_address=address, idempotency_key=generate_uuid(),
                                      relationships=create_relationship("depositAccount", account_id, "account"))

    return client.cards.create(request).data


@pytest.fixture()
def business_virtual_debit_card():
    account_id = create_deposit_account_for_business(client).data.id

    request = CreateBusinessVirtualDebitCard(full_name, "2001-08-10", address, phone, "richard@piedpiper.com",
                                             relationships=create_relationship("depositAccount", account_id, "account"))

    return client.cards.create(request).data


@pytest.fixture
def business_credit_card():
    account_id = create_credit_account_for_business(client).data.id

    request = CreateBusinessCreditCard(full_name, "2001-08-10", address, phone,
                                       "richard@piedpiper.com", shipping_address=address,
                                       idempotency_key=generate_uuid(),
                                       relationships=create_relationship("creditAccount", account_id, "account"))

    return client.cards.create(request).data


def test_create_individual_debit_card(individual_debit_card):
    assert individual_debit_card.type == "individualDebitCard"


def test_get_individual_debit_card(individual_debit_card):
    card_id = individual_debit_card.id
    response = client.cards.get(card_id)
    assert response.data.type == "individualDebitCard"


def test_list_cards():
    response = client.cards.list(ListCardParams(0, 1000))
    for card in response.data:
        assert card.type in card_types
        if card.attributes["status"] == "Inactive":
            res = requests.post(f"https://api.s.unit.sh/sandbox/cards/{card.id}/activate/", headers=headers)


def test_get_debit_card_include_customer(individual_debit_card):
    card_id = individual_debit_card.id
    response = client.cards.get(card_id, "customer")
    assert response.data.type in card_types and response.included is not None


def test_freeze_and_unfreeze_card():
    card_id = find_card_id({"status": "Active"})
    response = client.cards.freeze(card_id)
    assert response.data.attributes["status"] == "Frozen"
    response = client.cards.unfreeze(card_id)
    assert response.data.attributes["status"] != "Frozen"


def test_close_card():
    card_id = find_card_id({"status": "Active"})
    response = client.cards.close(card_id)
    assert response.data.attributes["status"] == "ClosedByCustomer"


def test_replace_card():
    card_id = find_card_id({"type": "individualDebitCard", "status": "Active"})
    _address = Address("1616 Pennsylvania Avenue Northwest", "Washington", "CA", "21500", "US")
    response = client.cards.replace(card_id, _address)
    assert response.data.type == "individualDebitCard"


def test_close_card():
    card_id = find_card_id({"status": "Active"})
    response = client.cards.close(card_id)
    assert response.data.type in card_types


def test_report_stolen_card():
    card_id = find_card_id({"status": "Active"})
    response = client.cards.report_stolen(card_id)
    assert response.data.type in card_types


def test_report_lost_card():
    card_id = find_card_id({"status": "Active"})
    response = client.cards.report_lost(card_id)
    assert response.data.type in card_types


def test_update_individual_card():
    card_id = find_card_id({"type": "individualDebitCard", "status": "Active"})
    _address = Address("1818 Pennsylvania Avenue Northwest", "Washington", "CA", "21500", "US")
    request = PatchIndividualDebitCard(card_id, _address, tags={"test": "updated"})
    response = client.cards.update(request)
    assert response.data.type == "individualDebitCard"
    assert response.data.attributes.get("tags").get("test") == "updated"


def test_update_business_card(business_debit_card):
    card_id = business_debit_card.id
    _address = Address("1818 Pennsylvania Avenue Northwest", "Washington", "CA", "21500", "US")
    request = PatchBusinessDebitCard(card_id, address=_address, tags={"test": "updated"})
    response = client.cards.update(request)
    assert response.data.type == "businessDebitCard"
    assert response.data.attributes.get("tags").get("test") == "updated"


def test_get_pin_status():
    response = client.cards.list()
    for card in response.data:
        if card.attributes["status"] != "Inactive":
            pin_status = client.cards.get_pin_status(card.id).data
            assert pin_status.type == "pinStatus"


def test_card_limits():
    card_id = find_card_id({"type": "individualDebitCard", "status": "Active"})
    response = client.cards.limits(card_id)
    assert response.data.type == "limits"


def test_create_business_debit_card(business_debit_card):
    assert business_debit_card.type == "businessDebitCard"


def test_create_business_virtual_debit_card(business_virtual_debit_card):
    assert business_virtual_debit_card.type == "businessVirtualDebitCard"


def test_create_business_credit_card(business_credit_card):
    assert business_credit_card.type == "businessCreditCard"


def test_create_business_virtual_credit_card():
    account_id = create_credit_account_for_business(client).data.id

    request = CreateBusinessVirtualCreditCard(full_name, "2001-08-10", address, phone, "richard@piedpiper.com",
                                              relationships=create_relationship("creditAccount", account_id, "account"))

    response = client.cards.create(request)
    assert response.data.type == "businessVirtualCreditCard"


def test_update_business_credit_card(business_credit_card):
    card_id = business_credit_card.id
    _address = Address("1818 Pennsylvania Avenue Northwest", "Washington", "CA", "21500", "US")
    request = PatchBusinessCreditCard(card_id, address=_address, tags={"test": "updated"})
    response = client.cards.update(request)
    assert response.data.type == "businessCreditCard"
    assert response.data.attributes.get("tags").get("test") == "updated"

