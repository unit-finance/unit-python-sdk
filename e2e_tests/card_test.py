import os
import unittest
from datetime import timedelta
from unit import Unit
from unit.models.card import CreateIndividualDebitCard, PatchIndividualDebitCard
from unit.models.account import *
from unit.models.application import CreateIndividualApplicationRequest

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)

card_types = ["individualDebitCard", "businessDebitCard", "individualVirtualDebitCard", "businessVirtualDebitCard"]


def find_card_id(criteria: Dict[str, str]):
    def filter_func(card):
        for key, value in criteria.items():
            if key not in card.attributes:
                if getattr(card,key) != value:
                    return False
            elif card.attributes[key] != value:
                return False
        return True

    response = client.cards.list()
    filtered = list(filter(filter_func, response.data))
    return filtered[0].id if len(filtered) > 0 else ""


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


def create_individual_debit_card():
    account_id = create_deposit_account().data.id
    request = CreateIndividualDebitCard(relationships={
        "account": {
            "data": {
                "type": "depositAccount",
                "id": account_id
            }
        }
    })
    return client.cards.create(request)


def test_create_individual_debit_card():
    response = create_individual_debit_card()
    assert response.data.type == "individualDebitCard"


def test_get_debit_card():
     card_id = create_individual_debit_card().data.id
     response = client.cards.get(card_id)
     assert response.data.type in card_types


def test_list_cards():
    response = client.cards.list()
    for card in response.data:
        assert card.type in card_types


def test_get_debit_card_include_customer():
     card_id = create_individual_debit_card().data.id
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
    address = Address("1616 Pennsylvania Avenue Northwest", "Washington", "CA", "21500", "US")
    response = client.cards.replace(card_id, address)
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
    address = Address("1818 Pennsylvania Avenue Northwest", "Washington", "CA", "21500", "US")
    request = PatchIndividualDebitCard(card_id, address)
    response = client.cards.update(request)
    assert response.data.type == "individualDebitCard"


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

