from api.application_resource import ApplicationResource
from api.customer_resource import CustomerResource
from api.account_resource import AccountResource
from api.card_resource import CardResource


class Unit(object):
    def __init__(self, api_url, token):
        self.applications = ApplicationResource(api_url, token)
        self.customers = CustomerResource(api_url, token)
        self.accounts = AccountResource(api_url, token)
        self.cards = CardResource(api_url, token)
