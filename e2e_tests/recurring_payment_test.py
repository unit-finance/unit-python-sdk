import os
import unittest
from unit import Unit
from unit.models.payment import *
from e2e_tests.account_test import create_deposit_account
from e2e_tests.counterparty_test import create_counterparty


token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)


def create_recurring_credit_ach_payment():
    account_id = create_deposit_account().data.id
    counterparty_id = create_counterparty().data.id

    request = CreateRecurringCreditAchPaymentRequest(200, "Rent-Apt15", CreateSchedule("Monthly", 16, 12),
                                                     {"account": Relationship("depositAccount", account_id),
                                                      "counterparty": Relationship("counterparty", counterparty_id)})
    return client.recurring_payments.create(request)


def test_create_recurring_credit_ach_payment():
    res = create_recurring_credit_ach_payment()
    assert res.data.type == "recurringCreditAchPayment"
