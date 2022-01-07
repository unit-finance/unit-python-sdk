import os
import unittest
from datetime import timedelta
from unit import Unit
from unit.models.card import CreateIndividualDebitCard, PatchIndividualDebitCard
from unit.models.account import *
from unit.models.application import CreateIndividualApplicationRequest


class CardE2eTests(unittest.TestCase):
    token = os.environ.get("token")
    client = Unit("https://api.s.unit.sh", token)
    card_types = ["individualDebitCard", "businessDebitCard", "individualVirtualDebitCard", "businessVirtualDebitCard"]

    def find_card_id(self, criteria: Dict[str, str]):
        def filter_func(card):
            for key, value in criteria.items():
                if key not in card.attributes:
                    if getattr(card,key) != value:
                        return False
                elif card.attributes[key] != value:
                    return False
            return True

        response = self.client.cards.list()
        filtered = list(filter(filter_func, response.data))
        return filtered[0].id if len(filtered) > 0 else ""

    def create_individual_customer(self):
        request = CreateIndividualApplicationRequest(
            FullName("Jhon", "Doe"), date.today() - timedelta(days=20 * 365),
            Address("1600 Pennsylvania Avenue Northwest", "Washington", "CA", "20500", "US"),
            "jone.doe1@unit-finance.com",
            Phone("1", "2025550108"), ssn="721074426",
        )
        response = self.client.applications.create(request)
        for key, value in response.data.relationships.items():
            if key == "customer":
                return value.id

        return ""

    def create_deposit_account(self):
        customer_id = self.create_individual_customer()
        request = CreateDepositAccountRequest("checking",
                                              {"customer": Relationship("customer", customer_id)},
                                              {"purpose": "checking"})
        return self.client.accounts.create(request)

    def create_individual_debit_card(self):
        account_id = self.create_deposit_account().data.id
        request = CreateIndividualDebitCard(relationships={
            "account": {
                "data": {
                    "type": "depositAccount",
                    "id": account_id
                }
            }
        })
        return self.client.cards.create(request)

    def test_create_individual_debit_card(self):
        response = self.create_individual_debit_card()
        self.assertTrue(response.data.type == "individualDebitCard")

    def test_get_debit_card(self):
         card_id = self.create_individual_debit_card().data.id
         response = self.client.cards.get(card_id)
         self.assertTrue(response.data.type in self.card_types)

    def test_list_cards(self):
        response = self.client.cards.list()
        for card in response.data:
            self.assertTrue(card.type in self.card_types)

    def test_freeze_and_unfreeze_card(self):
        card_id = self.find_card_id({"status": "Active"})
        response = self.client.cards.freeze(card_id)
        self.assertTrue(response.data.attributes["status"] == "Frozen")
        response = self.client.cards.unfreeze(card_id)
        self.assertTrue(response.data.attributes["status"] != "Frozen")

    def test_close_card(self):
        card_id = self.find_card_id({"status": "Active"})
        response = self.client.cards.close(card_id)
        self.assertTrue(response.data.attributes["status"] == "ClosedByCustomer")

    def test_replace_card(self):
        card_id = self.find_card_id({"type": "individualDebitCard", "status": "Active"})
        address = Address("1616 Pennsylvania Avenue Northwest", "Washington", "CA", "21500", "US")
        response = self.client.cards.replace(card_id, address)
        self.assertTrue(response.data.type == "individualDebitCard")

    def test_close_card(self):
        card_id = self.find_card_id({"status": "Active"})
        response = self.client.cards.close(card_id)
        self.assertTrue(response.data.type in self.card_types)

    def test_report_stolen_card(self):
        card_id = self.find_card_id({"status": "Active"})
        response = self.client.cards.report_stolen(card_id)
        self.assertTrue(response.data.type in self.card_types)

    def test_report_lost_card(self):
        card_id = self.find_card_id({"status": "Active"})
        response = self.client.cards.report_lost(card_id)
        self.assertTrue(response.data.type in self.card_types)

    def test_update_individual_card(self):
        card_id = self.find_card_id({"type": "individualDebitCard", "status": "Active"})
        address = Address("1818 Pennsylvania Avenue Northwest", "Washington", "CA", "21500", "US")
        request = PatchIndividualDebitCard(card_id, address)
        response = self.client.cards.update(request)
        self.assertTrue(response.data.type == "individualDebitCard")

    def test_get_pin_status(self):
        response = self.client.cards.list()
        for card in response.data:
            if card.attributes["status"] != "Inactive":
                pin_status = self.client.cards.get_pin_status(card.id).data
                self.assertTrue(pin_status.type == "pinStatus")


if __name__ == '__main__':
    unittest.main()
