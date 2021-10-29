from api.application_resource import ApplicationResource
from api.customer_resource import CustomerResource
from api.account_resource import AccountResource
from api.card_resource import CardResource
from api.transaction_resource import TransactionResource
from api.payment_resource import PaymentResource
from api.customerToken_resource import CustomerTokenResource
from api.webhook_resource import WebhookResource


class Unit(object):
    def __init__(self, api_url, token):
        self.applications = ApplicationResource(api_url, token)
        self.customers = CustomerResource(api_url, token)
        self.accounts = AccountResource(api_url, token)
        self.cards = CardResource(api_url, token)
        self.transactions = TransactionResource(api_url, token)
        self.payments = PaymentResource(api_url, token)
        self.customerTokens = CustomerTokenResource(api_url, token)
        self.webhooks = WebhookResource(api_url, token)
