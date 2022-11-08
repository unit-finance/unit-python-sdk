import os
import pytest
from unit import Unit
from unit.models.check_deposit import CreateCheckDepositRequest
from e2e_tests.helpers.helpers import create_relationship, create_deposit_account

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)


@pytest.fixture()
def check_deposit():
    account = create_deposit_account(client)
    return client.checkDeposits.create(
        CreateCheckDepositRequest(20000, create_relationship("depositAccount", account.data.id, "account"),
                                  "Check deposit")
    ).data


def test_create_check_deposit(check_deposit):
    assert check_deposit.type == "checkDeposit"


def test_list_and_get_check_deposits(check_deposit):
    assert check_deposit.type == "checkDeposit"

    response = client.checkDeposits.list()
    for c in response.data:
        assert c.type == "checkDeposit"
        res = client.checkDeposits.get(c.id)
        assert res.data.type == "checkDeposit"
