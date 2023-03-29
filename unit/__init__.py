from unit.api.application_resource import ApplicationResource
from unit.api.customer_resource import CustomerResource
from unit.api.account_resource import AccountResource
from unit.api.card_resource import CardResource
from unit.api.transaction_resource import TransactionResource
from unit.api.payment_resource import PaymentResource
from unit.api.received_payment_resource import ReceivedPaymentResource
from unit.api.statement_resource import StatementResource
from unit.api.customerToken_resource import CustomerTokenResource
from unit.api.counterparty_resource import CounterpartyResource
from unit.api.returnAch_resource import ReturnAchResource
from unit.api.applicationForm_resource import ApplicationFormResource
from unit.api.fee_resource import FeeResource
from unit.api.event_resource import EventResource
from unit.api.webhook_resource import WebhookResource
from unit.api.institution_resource import InstitutionResource
from unit.api.atmLocation_resource import AtmLocationResource
from unit.api.bill_pay_resource import BillPayResource
from unit.api.api_token_resource import APITokenResource
from unit.api.authorization_resource import AuthorizationResource
from unit.api.authorization_request_resource import AuthorizationRequestResource
from unit.api.account_end_of_day_resource import AccountEndOfDayResource
from unit.api.checkDeposit_resource import CheckDepositResource
from unit.api.dispute_resource import DisputeResource
from unit.api.reward_resource import RewardResource
from unit.api.repayment_resource import RepaymentResource

__all__ = ["api", "models", "utils"]

from unit.utils.configuration import Configuration


class Unit(object):
    def __init__(self, api_url=None, token=None, retries=1, timeout=120, configuration: Configuration = None):
        c = configuration if configuration else Configuration(api_url, token, retries, timeout)
        self.applications = ApplicationResource("applications", c)
        self.customers = CustomerResource("customers", c)
        self.accounts = AccountResource("accounts", c)
        self.cards = CardResource("cards", c)
        self.transactions = TransactionResource("transactions", c)
        self.payments = PaymentResource("payments", c)
        self.statements = StatementResource("statements", c)
        self.customerTokens = CustomerTokenResource("customers", c)
        self.counterparty = CounterpartyResource("counterparties", c)
        self.returnAch = ReturnAchResource("returns", c)
        self.applicationForms = ApplicationFormResource("application-forms", c)
        self.fees = FeeResource("fees", c)
        self.events = EventResource("events", c)
        self.webhooks = WebhookResource("webhooks", c)
        self.institutions = InstitutionResource("institutions", c)
        self.atmLocations = AtmLocationResource("atm-locations", c)
        self.billPays = BillPayResource("payments/billpay/billers", c)
        self.api_tokens = APITokenResource("users", c)
        self.authorizations = AuthorizationResource("authorizations", c)
        self.authorization_requests = AuthorizationRequestResource("authorization-requests", c)
        self.account_end_of_day = AccountEndOfDayResource("account-end-of-day", c)
        self.checkDeposits = CheckDepositResource("check-deposits", c)
        self.disputes = DisputeResource("disputes", c)
        self.rewards = RewardResource("rewards", c)
        self.received_payments = ReceivedPaymentResource("received-payments", c)
        self.repayments = RepaymentResource("repayments", c)
