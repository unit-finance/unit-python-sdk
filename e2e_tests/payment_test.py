import os
import unittest
from unit import Unit
from unit.models.payment import *
from e2e_tests.account_test import AccountE2eTests


class PaymentE2eTests(unittest.TestCase):
    token = os.environ.get("token")
    client = Unit("https://api.s.unit.sh", token)

    def create_book_payment(self):
        AccountTests = AccountE2eTests()

        account_id1 = AccountTests.create_deposit_account().data.id
        account_id2 = AccountTests.create_deposit_account().data.id

        request = CreateBookPaymentRequest(200, "Book payment", {"account": Relationship("depositAccount", account_id1),
                                                                 "counterpartyAccount": Relationship("depositAccount",
                                                                                                     account_id2)},
                                           tags={"purpose": "checking"},
                                           )
        return self.client.payments.create(request)

    def test_list_and_get_payments(self):
        payments_ids = []
        response = self.client.payments.list()

        for t in response.data:
            self.assertTrue("Payment" in t.type)
            payments_ids.append(t.id)

        for id in payments_ids:
            response = self.client.payments.get(id)
            self.assertTrue("Payment" in response.data.type)
    
    def test_list_and_get_payments_filter_by_type(self):
        payments_ids = []
        params = PaymentListParams(types=["AchPayment", "WirePayment"])
        response = self.client.payments.list(params)

        for t in response.data:
            self.assertTrue(t.type == "achPayment" or t.type == "wirePayment")
            payments_ids.append(t.id)

        for id in payments_ids:
            response = self.client.payments.get(id)
            self.assertTrue(response.data.type == "achPayment" or response.data.type == "wirePayment")

    def test_list_and_get_payments_filter_by_status(self):
        payments_ids = []
        params = PaymentListParams(statuses=["Pending", "Sent"])
        response = self.client.payments.list(params)

        for t in response.data:
            self.assertTrue(t.attributes["status"] == "Pending" or t.attributes["status"] == "Sent")
            payments_ids.append(t.id)

        for id in payments_ids:
            response = self.client.payments.get(id)
            self.assertTrue(response.data.attributes["status"] == "Pending" or response.data.attributes["status"] == "Sent")

    def test_create_book_payment(self):
        response = self.create_book_payment()
        self.assertTrue(response.data.type == "bookPayment")

    def test_update_book_payment(self):
        payment_id = self.create_book_payment().data.id
        tags = {"purpose": "test"}
        request = PatchBookPaymentRequest(payment_id, tags)
        response = self.client.payments.update(request)
        self.assertTrue(response.data.type == "bookPayment")


if __name__ == '__main__':
    unittest.main()
