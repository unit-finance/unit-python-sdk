import os
import unittest
from unit import Unit
from unit.models.bill_pay import *

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)

def test_get_billers():
    request = GetBillersParams("Electric")
    response = client.billPays.get(request)
    for b in response.data:
        assert b.type == "biller"

def test_get_billers_with_page_param():
    request = GetBillersParams("Electric", 1)
    response = client.billPays.get(request)
    for b in response.data:
        assert b.type == "biller"


