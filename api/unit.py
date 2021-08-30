from api.application_resource import ApplicationResource
from api.account_resource import AccountResource


class Unit(object):
    def __init__(self, api_url, token):
        self.applications = ApplicationResource(api_url, token)
        self.accounts = AccountResource(api_url, token)
