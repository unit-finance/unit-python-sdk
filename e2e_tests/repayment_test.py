import os
import typing

from unit import Unit
from unit.models.repayment import RepaymentType

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)


def test_list_repayments():
    res = client.repayments.list()
    for rp in res.data:
        assert rp.type in typing.get_args(RepaymentType)
