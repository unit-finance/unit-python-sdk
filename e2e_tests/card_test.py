import os
import unittest
from api.unit import Unit
from models.card import CreateIndividualDebitCard

class MyTestCase(unittest.TestCase):
    token = os.environ.get("token")
    client = Unit("https://api.s.unit.sh", token)
    card_types = ["individualDebitCard", "businessDebitCard", "individualVirtualDebitCard", "businessVirtualDebitCard"]

    # def test_create_individual_debit_card(self):
    #     request = CreateIndividualDebitCard(relationships={
    #         "account": {
    #             "data": {
    #                 "type": "depositAccount",
    #                 "id": "36099"
    #             }
    #         }
    #     })
    #     response = self.client.cards.create(request)
    #     self.assertTrue(response.data.type == "individualDebitCard")

    # def test_get_debit_card(self):
    #     response = self.client.cards.get("26070")
    #     self.assertTrue(response.data.type in self.card_types)

    def test_list_cards(self):
        response = self.client.cards.list()
        for card in response.data:
            self.assertTrue(card.type in self.card_types)


if __name__ == '__main__':
    unittest.main()
