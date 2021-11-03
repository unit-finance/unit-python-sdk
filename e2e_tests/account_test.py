import os
import unittest
from datetime import timedelta
from unit import Unit
from unit.models.account import *
from unit.models.application import CreateIndividualApplicationRequest


class AccountE2eTests(unittest.TestCase):
    token = os.environ.get("token")
    client = Unit("https://api.s.unit.sh", token)

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

    def test_create_deposit_account(self):
        response = self.create_deposit_account()
        self.assertTrue(response.data.type == "depositAccount")

    def test_create_joint_deposit_account(self):
        customer_id1 = self.create_individual_customer()
        customer_id2 = self.create_individual_customer()
        request = CreateDepositAccountRequest("checking",
                                              {"customers": RelationshipArray([
                                                Relationship("customer", customer_id1),
                                                Relationship("customer", customer_id2)])},
                                              {"purpose": "checking"})
        response = self.client.accounts.create(request)
        self.assertTrue(response.data.type == "depositAccount")

    def test_get_account(self):
        account_id = self.create_deposit_account().data.id
        response = self.client.accounts.get(account_id)
        self.assertTrue(response.data.type == "depositAccount")

    def test_list_accounts(self):
        response = self.client.accounts.list()
        for acc in response.data:
            self.assertTrue(acc.type == "depositAccount")

    def test_limits_account(self):
        account_id = self.create_deposit_account().data.id
        response = self.client.accounts.limits(account_id)
        self.assertTrue(response.data.type == "limits")

    def test_close_and_reopen_account(self):
        account_id = self.create_deposit_account().data.id
        response = self.client.accounts.close_account(account_id, "Fraud")
        self.assertTrue(response.data.type == "depositAccount")
        response = self.client.accounts.reopen_account(account_id)
        self.assertTrue(response.data.type == "depositAccount")

    def test_update_account(self):
        account_id = self.create_deposit_account().data.id
        request = PatchDepositAccountRequest(account_id, tags={
            "purpose": "tax",
            "trackUserId": "userId_fe6885b5815463b26f65e71095832bdd916890f7"})
        response = self.client.accounts.update(request)
        self.assertTrue(response.data.type == "depositAccount")


if __name__ == '__main__':
    unittest.main()
