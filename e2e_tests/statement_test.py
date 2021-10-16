import os
import unittest
from api.unit import Unit


class PaymentE2eTests(unittest.TestCase):
    token = os.environ.get("token")
    client = Unit("https://api.s.unit.sh", token)

    def test_list_and_get_statements(self):
        statements = self.client.statements.list().data
        for s in statements:
            self.assertTrue(s.type == "accountStatementDTO")
            html_statement = self.client.statements.get_html(s.id).data
            self.assertTrue('<!DOCTYPE html>' in html_statement)
            pdf_statement = self.client.statements.get_pdf(s.id).data
            self.assertTrue('PDF' in pdf_statement)


if __name__ == '__main__':
    unittest.main()
