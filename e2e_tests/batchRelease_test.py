import os
import unittest
from api.unit import Unit
from models.batchRelease import *


class BatchReleaseE2eTests(unittest.TestCase):
    token = os.environ.get("token")
    client = Unit("https://api.s.unit.sh", token)

    def test_create_batch_releases(self):

        request1 = CreateBatchReleaseRequest(3000, "BATCH PYMT", "Richard Hendricks",
                                             Address("5230 Newell Rd", "Palo Alto", "CA", "94303", "US"),
                                             "123456798", {"batchAccount": Relationship("batchAccount", "27573"),
                                                                 "receiver": Relationship("depositAccount",
                                                                                                     "27573")})
        request2 = CreateBatchReleaseRequest(2000, "Purchase", "Peter Parker",
                                             Address("5230 Newell Rd", "Palo Alto", "CA", "94303", "US"),
                                             "5324131257", {"batchAccount": Relationship("batchAccount", "27573"),
                                                                 "receiver": Relationship("depositAccount",
                                                                                                     "27573")})

        response = self.client.batchRelease.create([request1, request2])
        self.assertTrue(response.data.type == "batchRelease")



if __name__ == '__main__':
    unittest.main()
