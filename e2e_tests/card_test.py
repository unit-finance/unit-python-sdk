import os
import unittest
from datetime import date, timedelta
from api.unit import Unit
from models.card import CreateIndividualDebitCard, PatchIndividualDebitCard
from models.account import *
from models.application import CreateIndividualApplicationRequest


class CardE2eTests(unittest.TestCase):
    token = os.environ.get("token")
    client = Unit("https://api.s.unit.sh", token)
    card_types = ["individualDebitCard", "businessDebitCard", "individualVirtualDebitCard", "businessVirtualDebitCard"]

    def get_card_id(self, opt_dict: dict[str, str]):
        response = self.client.cards.list()
        for card in response.data:
            cond = True
            for key, value in opt_dict.items():
                if getattr(card, key) != value:
                    cond = False

            if cond:
                return card.id

        return ""

    def get_new_customer(self):
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
        customer_id = self.get_new_customer()
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
        card_id = self.get_card_id({"status": "Active"})
        response = self.client.cards.freeze_card(card_id)
        self.assertTrue(response.data.status == "Frozen")
        response = self.client.cards.unfreeze_card(card_id)
        self.assertTrue(response.data.status != "Frozen")

    def test_close_card(self):
        card_id = self.get_card_id({"status": "Active"})
        response = self.client.cards.close_card(card_id)
        self.assertTrue(response.data.status == "ClosedByCustomer")

    def test_replace_card(self):
        card_id = self.get_card_id({"type": "individualDebitCard", "status": "Active"})
        address = Address("1616 Pennsylvania Avenue Northwest", "Washington", "CA", "21500", "US")
        response = self.client.cards.replace_card(card_id, address)
        self.assertTrue(response.data.type == "individualDebitCard")

    def test_close_card(self):
        card_id = self.get_card_id({"status": "Active"})
        response = self.client.cards.close_card(card_id)
        self.assertTrue(response.data.type in self.card_types)

    def test_report_stolen_card(self):
        card_id = self.get_card_id({"status": "Active"})
        response = self.client.cards.report_stolen(card_id)
        self.assertTrue(response.data.type in self.card_types)

    def test_report_lost_card(self):
        card_id = self.get_card_id({"status": "Active"})
        response = self.client.cards.report_lost(card_id)
        self.assertTrue(response.data.type in self.card_types)

    def test_update_individual_card(self):
        card_id = self.get_card_id({"type": "individualDebitCard", "status": "Active"})
        address = Address("1818 Pennsylvania Avenue Northwest", "Washington", "CA", "21500", "US")
        request = PatchIndividualDebitCard(card_id, address)
        response = self.client.cards.update(request)
        self.assertTrue(response.data.type == "individualDebitCard")


if __name__ == '__main__':
    unittest.main()
