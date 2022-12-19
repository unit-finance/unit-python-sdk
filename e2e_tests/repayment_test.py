import os
import typing

from unit import Unit
from unit.models.account import CloseAccountRequest
from unit.models.repayment import RepaymentType, CreateBookRepaymentRequest, CreateAchRepaymentRequest
from e2e_tests.helpers.helpers import create_deposit_account, create_credit_account_for_business, \
    create_relationship, generate_uuid, create_business_credit_card, create_counterparty, create_counterparty_with_token

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)


def close_account(account_id, _type="closeAccount"):
    close_req = CloseAccountRequest(account_id, _type=_type)
    close_res = client.accounts.close_account(close_req)
    assert close_res.data


def test_create_book_repayment():
    account_id = create_deposit_account(client).data.id
    credit_account_id = create_credit_account_for_business(client).data.id
    counterparty_account_id = create_deposit_account(client).data.id

    relationships = {}
    relationships.update(create_relationship("depositAccount", "1060441", "account"))
    relationships.update(create_relationship("creditAccount", "1060442"))
    relationships.update(create_relationship("account", "1060443", "counterpartyAccount"))

    #   card = create_business_credit_card(client, credit_account_id).data for simulation

    req = CreateBookRepaymentRequest("test", 50, relationships, transaction_summary_override="override",
                                     idempotency_key=generate_uuid())

    res = client.repayments.create(req)
    assert res.data.type == "bookRepayment"

    close_account(account_id)
    close_account(credit_account_id, "creditAccountClose")
    close_account(counterparty_account_id)


def test_create_ach_repayment():
    account_id = create_deposit_account(client).data.id
    credit_account_id = create_credit_account_for_business(client).data.id
    counterparty_id = create_counterparty_with_token(client,
                                                     "").data.id

    relationships = {}
    relationships.update(create_relationship("depositAccount", "1060441", "account"))
    relationships.update(create_relationship("creditAccount", "1060442"))
    relationships.update(create_relationship("counterparty", counterparty_id))

    req = CreateAchRepaymentRequest("test", 50, relationships, idempotency_key=generate_uuid())

    res = client.repayments.create(req)
    assert res.data.type == "achRepayment"

    close_account(account_id, "closeAccount")
    close_account(credit_account_id)
    client.counterparty.delete(counterparty_id)


def test_list_repayments():
    res = client.repayments.list()
    for rp in res.data:
        assert rp.type in typing.get_args(RepaymentType)

