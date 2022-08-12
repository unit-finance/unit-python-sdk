import os
import unittest
from unit import Unit
from unit.models.account_end_of_day import *

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)

def test_list_account_end_of_day():
    params = ListAccountEndOfDayParams(10, 0, account_id="27573")
    response = client.account_end_of_day.list(params)
    for a in response.data:
        assert a.type == "accountEndOfDay"

