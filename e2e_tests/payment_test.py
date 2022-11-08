import os
import unittest
import pytest

from e2e_tests.helpers.helpers import create_deposit_account
from unit import Unit
from unit.models.payment import *


token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)


@pytest.fixture
def book_payment():
    account_id1 = create_deposit_account(client).data.id
    account_id2 = create_deposit_account(client).data.id

    request = CreateBookPaymentRequest(200, "Book payment", {"account": Relationship("depositAccount", account_id1),
                                                             "counterpartyAccount": Relationship("depositAccount",
                                                                                                 account_id2)},
                                       tags={"purpose": "checking"},
                                       )
    return client.payments.create(request).data


def test_list_and_get_payments():
    payments_ids = []

    response = client.payments.list()

    for t in response.data:
        assert "Payment" in t.type
        payments_ids.append(t.id)

    for id in payments_ids:
        response = client.payments.get(id)
        assert "Payment" in response.data.type


def test_create_book_payment(book_payment):
    assert book_payment.type == "bookPayment"


def test_list_and_get_payments_filter_by_type():
    payments_ids = []
    params = ListPaymentParams(type=["AchPayment", "WirePayment"])
    response = client.payments.list(params)

    for t in response.data:
        assert t.type == "achPayment" or t.type == "wirePayment"
        payments_ids.append(t.id)

    for id in payments_ids:
        response = client.payments.get(id)
        assert response.data.type == "achPayment" or response.data.type == "wirePayment"


def test_list_and_get_payments_filter_by_status():
    payments_ids = []
    params = ListPaymentParams(status=["Pending", "Sent"])
    response = client.payments.list(params)

    for t in response.data:
        assert t.attributes["status"] == "Pending" or t.attributes["status"] == "Sent"
        payments_ids.append(t.id)

    for id in payments_ids:
        response = client.payments.get(id)
        assert response.data.attributes["status"] == "Pending" or response.data.attributes["status"] == "Sent"


def test_update_book_payment(book_payment):
    payment_id = book_payment.id
    tags = {"purpose": "test"}
    request = PatchBookPaymentRequest(payment_id, tags)
    response = client.payments.update(request)
    assert response.data.type == "bookPayment"
