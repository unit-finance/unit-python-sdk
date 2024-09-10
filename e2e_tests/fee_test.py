import os
import requests
from unit import Unit
from unit.models.fee import *
from unit.models.codecs import UnitEncoder
from e2e_tests.account_test import create_deposit_account

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)

def test_create_individual_application():
    deposit_account_id = create_deposit_account().data.id

    request = CreateFeeRequest(150, "test fee", {"account": Relationship("depositAccount", deposit_account_id)})

    headers = {
            "content-type": "application/vnd.api+json",
            "authorization": f"Bearer {token}",
            "user-agent": "unit-python-sdk"
    }

    data = {
       "data": {
                "type": "achReceivedPayment",
                "attributes": {
                "amount": 10000,
                "direction": "Credit",
                "description": "Payment from Sandbox",
                "companyName": "Sandbox",
                "completionDate": datetime.now().strftime("%Y-%m-%d")
                },
                "relationships": {
                "account": {
                    "data": {
                    "type": "depositAccount",
                    "id": deposit_account_id
                    }
                }
            }
        }
    }

    receivedPaymentRes = requests.post(f"https://api.s.unit.sh/sandbox/received-payments", data=json.dumps(data, cls=UnitEncoder),
                        headers=headers)

    receivedPaymentId = receivedPaymentRes.json()["data"]["id"]
    requests.post(f"https://api.s.unit.sh/sandbox/received-payments/{receivedPaymentId}/complete", headers=headers)

    response = client.fees.create(request)
    assert response.data.type == "fee"


