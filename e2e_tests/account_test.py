import os
import unittest
from datetime import datetime, date, timedelta
from api.unit import Unit
from models.account import *
from models.application import CreateIndividualApplicationRequest


class AccountE2eTests(unittest.TestCase):
    token = os.environ.get("token")
    client = Unit("https://api.s.unit.sh", token)

    def get_open_account(self):
        response = self.client.accounts.list()
        for acc in response.data:
            if acc.status == "Open" and acc.balance == 0 and acc.hold == 0:
                return acc.id

        return ""

    def get_closed_account(self):
        response = self.client.accounts.list()
        for acc in response.data:
            if acc.status == "Closed":
                return acc.id

        return ""

    def create_application(self):
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

    def test_create_deposit_account(self):
        request = CreateDepositAccountRequest("checking",
                                              {"customer": Relationship("customer", self.create_application())},
                                              {"purpose": "checking"})
        response = self.client.accounts.create(request)
        self.assertTrue(response.data.type == "depositAccount")

    def test_create_joint_deposit_account(self):
        request = CreateDepositAccountRequest("checking",
                                              {"customers": [Relationship("customer", self.create_application()),
                                                            Relationship("customer", self.create_application())]},
                                              {"purpose": "checking"})
        response = self.client.accounts.create(request)
        self.assertTrue(response.data.type == "depositAccount")

    def test_get_account(self):
        response = self.client.accounts.get(self.get_open_account())
        self.assertTrue(response.data.type == "depositAccount")

    def test_list_accounts(self):
        response = self.client.accounts.list()
        for acc in response.data:
            self.assertTrue(acc.type == "depositAccount")

    def test_limits_account(self):
        response = self.client.accounts.limits(self.get_open_account())
        self.assertTrue(response.data.type == "limits")

    def test_close_account(self):
        response = self.client.accounts.close_account(self.get_open_account(), "Fraud")
        self.assertTrue(response.data.type == "depositAccount")

    def test_reopen_account(self):
        response = self.client.accounts.reopen_account(self.get_closed_account())
        self.assertTrue(response.data.type == "depositAccount")

    def test_update_account(self):
        request = PatchDepositAccountRequest(self.get_open_account(), tags={
            "purpose": "tax",
            "trackUserId": "userId_fe6885b5815463b26f65e71095832bdd916890f7"})
        response = self.client.accounts.update(request)
        self.assertTrue(response.data.type == "depositAccount")


if __name__ == '__main__':
    unittest.main()
