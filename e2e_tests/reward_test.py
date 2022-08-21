import os

from e2e_tests.account_test import create_deposit_account
from unit import Unit
from unit.models.reward import CreateRewardRequest

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)


def test_create_reward():
    account_id = create_deposit_account().data.id
    req = CreateRewardRequest(3000, "Reward for transaction #5678", account_id, tags={"test": "rewards"})
    res = client.rewards.create(req)
    assert res.data.type == "reward"
    assert res.data.attributes["amount"] == 3000
    assert res.data.attributes["description"] == "Reward for transaction #5678"

    reward_id = res.data.id

    reward = client.rewards.get(reward_id, "account, transaction, customer")
    assert reward.data.type == "reward"


def test_list_rewards():
    res = client.rewards.list()
    for r in res.data:
        assert r.type == "reward"

