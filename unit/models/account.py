from unit.utils import date_utils

from unit.models import *

AccountStatus = Literal["Open", "Closed"]
CloseReason = Literal["ByCustomer", "Fraud"]


class DepositAccountDTO(object):
    def __init__(self, id: str, created_at: datetime, name: str, deposit_product: str, routing_number: str,
                 account_number: str, currency: str, balance: int, hold: int, available: int, status: AccountStatus,
                 tags: Optional[Dict[str, str]], close_reason: Optional[CloseReason],
                 relationships: Optional[Dict[str, Relationship]]):
        self.id = id
        self.type = "depositAccount"
        self.attributes = {"name": name, "createdAt": created_at, "depositProduct": deposit_product,
                           "routingNumber": routing_number, "accountNumber": account_number, "currency": currency,
                           "balance": balance, "hold": hold, "available": available, "status": status,
                           "closeReason": close_reason, "tags": tags}
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return DepositAccountDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), attributes["name"], attributes["depositProduct"],
            attributes["routingNumber"], attributes["accountNumber"], attributes["currency"], attributes["balance"],
            attributes["hold"], attributes["available"], attributes["status"], attributes.get("tags"),
            attributes.get("closeReason"), relationships
        )


AccountDTO = Union[DepositAccountDTO]


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
                "type": "depositAccount",
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
        json.dumps(self.to_json_api())


class PatchDepositAccountRequest(UnitRequest):
    def __init__(self, account_id: str, deposit_product: Optional[str] = None, tags: Optional[Dict[str, str]] = None):
        self.account_id = account_id
        self.deposit_product = deposit_product
        self.tags = tags

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "depositAccount",
                "attributes": {}
            }
        }

        if self.deposit_product:
            payload["data"]["attributes"]["depositProduct"] = self.deposit_product

        if self.tags:
            payload["data"]["attributes"]["tags"] = self.tags

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())


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
        return AccountAchLimits(AchLimits.from_json_api(data["limits"]), AchTotals.from_json_api(data["totalsDaily"]),
                         AchTotals.from_json_api(data["totalsMonthly"]))


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
        return AccountCardLimits(CardLimits.from_json_api(data["limits"]),
                                 CardTotals.from_json_api(data["totalsDaily"]))


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
        return CheckDepositAccountLimits(CheckDepositLimits.from_json_api(data["limits"]), data["totalsDaily"],
                                         data["totalsMonthly"])


class AccountLimitsDTO(object):
    def __init__(self, ach: AccountAchLimits, card: AccountCardLimits, check_deposit: CheckDepositAccountLimits):
        self.type = "limits"
        self.attributes = {"ach": ach, "card": card, "checkDeposit": check_deposit}

    @staticmethod
    def from_json_api(attributes):
        return AccountLimitsDTO(AccountAchLimits.from_json_api(attributes["ach"]),
                                AccountCardLimits.from_json_api(attributes["card"]),
                                CheckDepositAccountLimits.from_json_api(attributes["checkDeposit"]))


class CloseAccountRequest(UnitRequest):
    def __init__(self, account_id: str, reason: Optional[Literal["ByCustomer", "Fraud"]] = "ByCustomer"):
        self.account_id = account_id
        self.reason = reason

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "accountClose",
                "attributes": {
                    "reason": self.reason,
                }
            }
        }

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())


class ListAccountParams(UnitParams):
    def __init__(self, offset: int = 0, limit: int = 100, customer_id: Optional[str] = None,
                 tags: Optional[object] = None, include: Optional[str] = None):
        self.offset = offset
        self.limit = limit
        self.customer_id = customer_id
        self.tags = tags
        self.include = include
    
    def to_dict(self) -> Dict:
        parameters = {"page[limit]": self.limit, "page[offset]": self.offset}
        if self.customer_id:
            parameters["filter[customerId]"] = self.customer_id
        if self.tags:
            parameters["filter[tags]"] = self.tags
        if self.include:
            parameters["include"] = self.include
        return parameters
