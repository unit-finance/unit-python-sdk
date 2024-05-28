from unit.utils import date_utils
from unit.models import *

AccountStatus = Literal["Open", "Frozen", "Closed"]
CloseReason = Literal["ByCustomer", "Fraud"]
FraudReason = Literal["ACHActivity", "CardActivity", "CheckActivity", "ApplicationHistory", "AccountActivity",
                      "ClientIdentified", "IdentityTheft", "LinkedToFraudulentCustomer"]

CreditAccountType = "creditAccount"
DepositAccountType = "depositAccount"
AccountTypes = Literal[CreditAccountType, DepositAccountType]


class DepositAccountDTO(object):
    def __init__(self, _id: str, created_at: datetime, updated_at: Optional[datetime], name: str, deposit_product: str,
                 routing_number: str, account_number: str, currency: str, balance: int, hold: int, available: int,
                 status: AccountStatus, tags: Optional[Dict[str, str]], close_reason: Optional[CloseReason],
                 relationships: Optional[Dict[str, Relationship]]):
        self.id = _id
        self.type = DepositAccountType
        self.attributes = {"name": name, "createdAt": created_at, "updatedAt": updated_at,
                           "depositProduct": deposit_product, "routingNumber": routing_number,
                           "accountNumber": account_number, "currency": currency, "balance": balance,
                           "hold": hold, "available": available, "status": status, "closeReason": close_reason,
                           "tags": tags}
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return DepositAccountDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), date_utils.to_datetime(attributes.get("updatedAt")),
            attributes["name"], attributes["depositProduct"], attributes["routingNumber"], attributes["accountNumber"],
            attributes["currency"], attributes["balance"], attributes["hold"], attributes["available"],
            attributes["status"], attributes.get("tags"), attributes.get("closeReason"), relationships
        )


class CreditAccountDTO(object):
    def __init__(self, _id: str, created_at: datetime, updated_at: Optional[datetime], name: str, credit_terms: str,
                 currency: str, credit_limit: int, balance: int, hold: int, available: int,
                 tags: Optional[Dict[str, str]], status: AccountStatus, freeze_reason: Optional[str],
                 close_reason: Optional[str], close_reason_text: Optional[str], fraud_reason: Optional[FraudReason],
                 relationships: Optional[Dict[str, Relationship]]):
        self.id = _id
        self.type = CreditAccountType
        self.attributes = {"createdAt": created_at, "updatedAt": updated_at, "name": name, "status": status,
                           "creditTerms": credit_terms, "currency": currency, "creditLimit": credit_limit,
                           "balance": balance, "hold": hold, "available": available, "tags": tags,
                           "freezeReason": freeze_reason, "closeReason": close_reason,
                           "closeReasonText": close_reason_text, "fraudReason": fraud_reason}
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CreditAccountDTO(_id, date_utils.to_datetime(attributes["createdAt"]),
                                date_utils.to_datetime(attributes.get("updatedAt")), attributes["name"],
                                attributes["creditTerms"], attributes["currency"], attributes["creditLimit"],
                                attributes["balance"], attributes["hold"], attributes["available"],
                                attributes.get("tags"), attributes["status"], attributes.get("freezeReason"),
                                attributes.get("closeReason"), attributes.get("closeReasonText"),
                                attributes.get("fraudReason"), relationships)


AccountDTO = Union[DepositAccountDTO, CreditAccountDTO]


class CreateDepositAccountRequest(UnitRequest):
    def __init__(self, deposit_product: str, relationships: Optional[Dict[str, Union[Relationship, RelationshipArray]]],
                 tags: Optional[Dict[str, str]] = None, idempotency_key: Optional[str] = None):
        self.deposit_product = deposit_product
        self.tags = tags
        self.idempotency_key = idempotency_key
        self.relationships = relationships

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": DepositAccountType,
                "attributes": {
                    "depositProduct": self.deposit_product,
                },
                "relationships": self.relationships
            }
        }

        if self.tags:
            payload["data"]["attributes"]["tags"] = self.tags

        if self.idempotency_key:
            payload["data"]["attributes"]["idempotencyKey"] = self.idempotency_key

        return payload

    def __repr__(self):
        return json.dumps(self.to_json_api())


class CreateCreditAccountRequest(UnitRequest):
    def __init__(self, credit_terms: str, credit_limit: int, relationships: Dict[str, Relationship],
                 tags: Optional[Dict[str, str]] = None, idempotency_key: Optional[str] = None):
        self.credit_terms = credit_terms
        self.credit_limit = credit_limit
        self.tags = tags
        self.idempotency_key = idempotency_key
        self.relationships = relationships

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "creditAccount",
                "attributes": {
                    "creditTerms": self.credit_terms,
                    "creditLimit": self.credit_limit
                },
                "relationships": self.relationships
            }
        }

        if self.tags:
            payload["data"]["attributes"]["tags"] = self.tags

        if self.idempotency_key:
            payload["data"]["attributes"]["idempotencyKey"] = self.idempotency_key

        return payload

    def __repr__(self):
        return json.dumps(self.to_json_api())


CreateAccountRequest = Union[CreateDepositAccountRequest, CreateCreditAccountRequest]


class PatchDepositAccountRequest(UnitRequest):
    def __init__(self, account_id: str, deposit_product: Optional[str] = None, tags: Optional[Dict[str, str]] = None):
        self.account_id = account_id
        self.deposit_product = deposit_product
        self.tags = tags

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": DepositAccountType,
                "attributes": {}
            }
        }

        if self.deposit_product:
            payload["data"]["attributes"]["depositProduct"] = self.deposit_product

        if self.tags:
            payload["data"]["attributes"]["tags"] = self.tags

        return payload

    def __repr__(self):
        return json.dumps(self.to_json_api())


class PatchCreditAccountRequest(UnitRequest):
    def __init__(self, account_id: str, tags: Optional[Dict[str, str]] = None, credit_limit: Optional[int] = None):
        self.account_id = account_id
        self.tags = tags
        self.credit_limit = credit_limit

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": CreditAccountType,
                "attributes": {}
            }
        }

        if self.tags:
            payload["data"]["attributes"]["tags"] = self.tags

        if self.credit_limit:
            payload["data"]["attributes"]["creditLimit"] = self.credit_limit

        return payload

    def __repr__(self):
        return json.dumps(self.to_json_api())

PatchAccountRequest = Union[PatchDepositAccountRequest, PatchCreditAccountRequest]


class AchTotals(object):
    def __init__(self, debits: int, credits: int):
        self.debits = debits
        self.credits = credits

    @staticmethod
    def from_json_api(data: Dict):
        return AchTotals(data["debits"], data["credits"])


class AchLimits(object):
    def __init__(self, daily_debit: int, daily_credit: int, monthly_debit: int, monthly_credit: int,
                 daily_debit_soft: int, monthly_debit_soft: int):
        self.daily_debit = daily_debit
        self.daily_credit = daily_credit
        self.monthly_debit = monthly_debit
        self.monthly_credit = monthly_credit
        self.daily_debit_soft = daily_debit_soft
        self.monthly_debit_soft = monthly_debit_soft

    @staticmethod
    def from_json_api(data: Dict):
        return AchLimits(data["dailyDebit"], data["dailyCredit"], data["monthlyDebit"], data["monthlyCredit"],
                         data["dailyDebitSoft"], data["monthlyDebitSoft"])


class AccountAchLimits(object):
    def __init__(self, limits: AchLimits, totals_daily: AchTotals, totals_monthly: AchTotals):
        self.limits = limits
        self.totals_daily = totals_daily
        self.totals_monthly = totals_monthly

    @staticmethod
    def from_json_api(data: Dict):
        if data:
            return AccountAchLimits(AchLimits.from_json_api(data["limits"]),
                                    AchTotals.from_json_api(data["totalsDaily"]),
                                    AchTotals.from_json_api(data["totalsMonthly"]))
        return None


class CardLimits(object):
    def __init__(self, daily_withdrawal: int, daily_deposit: int, daily_purchase: int, daily_card_transaction: int):
        self.daily_withdrawal = daily_withdrawal
        self.daily_deposit = daily_deposit
        self.daily_purchase = daily_purchase
        self.daily_card_transaction = daily_card_transaction

    @staticmethod
    def from_json_api(data: Dict):
        return CardLimits(data["dailyWithdrawal"], data["dailyDeposit"],
                          data["dailyPurchase"], data["dailyCardTransaction"])


class CardTotals(object):
    def __init__(self, withdrawals: int, deposits: int, purchases: int, card_transactions: int):
        self.withdrawals = withdrawals
        self.deposits = deposits
        self.purchases = purchases
        self.card_transactions = card_transactions

    @staticmethod
    def from_json_api(data: Dict):
        return CardTotals(data["withdrawals"], data["deposits"], data["purchases"], data["cardTransactions"])


class AccountCardLimits(object):
    def __init__(self, limits: CardLimits, totals_daily: CardTotals):
        self.limits = limits
        self.totals_daily = totals_daily

    @staticmethod
    def from_json_api(data: Dict):
        if data:
            return AccountCardLimits(CardLimits.from_json_api(data["limits"]),
                                     CardTotals.from_json_api(data["totalsDaily"]))
        return None


class CheckDepositLimits(object):
    def __init__(self, daily: int, monthly: int, daily_soft: int, monthly_soft: int):
        self.daily = daily
        self.monthly = monthly
        self.daily_soft = daily_soft
        self.monthly_soft = monthly_soft

    @staticmethod
    def from_json_api(data: Dict):
        return CheckDepositLimits(data["daily"], data["monthly"], data["dailySoft"], data["monthlySoft"])


class CheckDepositAccountLimits(object):
    def __init__(self, limits: CheckDepositLimits, totals_daily: int, totals_monthly: int):
        self.limits = limits
        self.totals_daily = totals_daily
        self.totals_monthly = totals_monthly

    @staticmethod
    def from_json_api(data: Dict):
        if data:
            return CheckDepositAccountLimits(CheckDepositLimits.from_json_api(data["limits"]), data["totalsDaily"],
                                             data["totalsMonthly"])
        return None


class AccountLimitsDTO(object):
    def __init__(self, _id: str, _type: str, card: AccountCardLimits):
        self.id = _id
        self.type = _type
        self.attributes = {"card": card}


class DepositAccountLimitsDTO(AccountLimitsDTO):
    def __init__(self, ach: AccountAchLimits, card: AccountCardLimits, check_deposit: CheckDepositAccountLimits,
                 _id: str, _type: str):
        super().__init__(_id, _type, card)
        self.attributes = {"ach": ach, "checkDeposit": check_deposit}

    @staticmethod
    def from_json_api(_id, _type, attributes):
        return DepositAccountLimitsDTO(AccountAchLimits.from_json_api(attributes.get("ach")),
                                       AccountCardLimits.from_json_api(attributes.get("card")),
                                       CheckDepositAccountLimits.from_json_api(
                                           attributes.get("checkDeposit")), _id, _type)


class CreditAccountLimitsDTO(AccountLimitsDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes):
        return CreditAccountLimitsDTO(_id, _type, AccountCardLimits.from_json_api(attributes.get("card")))


AccountCloseReason = Literal["ByCustomer", "Fraud", "NegativeBalance", "Overdue", "ByBank"]
AccountCloseType = Literal["depositAccountClose", "creditAccountClose"]
BankReason = Literal["ProhibitedBusiness", "MissingCddEdd", "NonUsOperations", "SuspectedFraud"]


class CloseAccountRequest(UnitRequest):
    def __init__(self, account_id: str, reason: Optional[AccountCloseReason] = "ByCustomer",
                 fraud_reason: Optional[FraudReason] = None, _type: AccountCloseType = "depositAccountClose",
                 bank_reason: Optional[BankReason] = None):
        self.account_id = account_id
        self.reason = reason
        self.fraud_reason = fraud_reason
        self._type = _type
        self.bank_reason = bank_reason

    def to_json_api(self) -> Dict:
        return super().to_payload(self._type, ignore=["_type", "account_id"])

    def __repr__(self):
        return json.dumps(self.to_json_api())


class ListAccountParams(UnitParams):
    def __init__(self, offset: int = 0, limit: int = 100, customer_id: Optional[str] = None,
                 tags: Optional[Dict[str, str]] = None, include: Optional[str] = None,
                 status: Optional[AccountStatus] = None, from_balance: Optional[int] = None,
                 to_balance: Optional[int] = None, _type: Optional[AccountTypes] = None):
        self.offset = offset
        self.limit = limit
        self.customer_id = customer_id
        self.tags = tags
        self.include = include
        self.status = status
        self.from_balance = from_balance
        self.to_balance = to_balance
        self._type = _type
    
    def to_dict(self) -> Dict:
        parameters = {"page[limit]": self.limit, "page[offset]": self.offset}
        if self.customer_id:
            parameters["filter[customerId]"] = self.customer_id
        if self.tags:
            parameters["filter[tags]"] = json.dumps(self.tags)
        if self.include:
            parameters["include"] = self.include
        if self.status:
            for idx, status_filter in enumerate(self.status):
                parameters[f"filter[status][{idx}]"] = status_filter
        if self._type:
            parameters[f"filter[type]"] = self._type
        if self.from_balance:
            parameters["filter[fromBalance]"] = self.from_balance
        if self.to_balance:
            parameters["filter[toBalance]"] = self.to_balance
        return parameters


class AccountOwnersRequest(UnitRequest):
    def __init__(self, account_id: str, customers: RelationshipArray):
        self.account_id = account_id
        self.customers = customers

    def to_json_api(self) -> Dict:
        return self.customers.to_dict()

    def __repr__(self):
        return json.dumps(self.to_json_api())


class AccountDepositProductDTO(object):
    def __init__(self, name: str):
        self.type = "accountDepositProduct"
        self.attributes = {"name": name}

    @staticmethod
    def from_json_api(attributes):
        return AccountDepositProductDTO(attributes["name"])


class FreezeAccountRequest(UnitRequest):
    def __init__(self, account_id: str, reason: Literal["Fraud", "Other"], reason_text: Optional[str] = None):
        self.account_id = account_id
        self.reason = reason
        self.reason_text = reason_text

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "accountFreeze",
                "attributes": {
                    "reason": self.reason,
                }
            }
        }

        if self.reason_text:
            payload["data"]["attributes"]["reasonText"] = self.reason_text

        return payload

    def __repr__(self) -> str:
        return json.dumps(self.to_json_api())
