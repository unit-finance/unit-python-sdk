from unit.utils import date_utils
from unit.models import *

AchStatus = Literal["Pending", "Rejected", "Clearing", "Sent", "Canceled", "Returned"]
PaymentTypes = Literal["AchPayment", "BookPayment", "WirePayment", "BillPayment"]
PaymentDirections = Literal["Debit", "Credit"]


class BasePayment(object):
    def __init__(self, id: str, created_at: datetime, direction: PaymentDirections, description: str, amount: int,
                 reason: Optional[str], tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        self.id = id
        self.attributes = {"createdAt": created_at, "direction": direction, "description": description,
                           "amount": amount, "reason": reason, "tags": tags}
        self.relationships = relationships

class AchPaymentDTO(BasePayment):
    def __init__(self, id: str, created_at: datetime, status: AchStatus, counterparty: Counterparty, direction: str,
                 description: str, amount: int, addenda: Optional[str], reason: Optional[str],
                 settlement_date: Optional[datetime], tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BasePayment.__init__(self, id, created_at, direction, description, amount, reason, tags, relationships)
        self.type = 'achPayment'
        self.attributes["status"] = status
        self.attributes["counterparty"] = counterparty
        self.attributes["addenda"] = addenda
        self.settlement_date = settlement_date

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        settlement_date = date_utils.to_date(attributes.get("settlementDate")) if attributes.get("settlementDate") else None
        return AchPaymentDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["status"],
                             attributes["counterparty"], attributes["direction"], attributes["description"],
                             attributes["amount"], attributes.get("addenda"), attributes.get("reason"), settlement_date,
                             attributes.get("tags"), relationships)

class BookPaymentDTO(BasePayment):
    def __init__(self, id: str, created_at: datetime, status: str, direction: Optional[str], description: str, amount: int,
                 reason: Optional[str], tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BasePayment.__init__(self, id, created_at, direction, description, amount, reason, tags, relationships)
        self.type = 'bookPayment'
        self.attributes["status"] = status

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return BookPaymentDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["status"],
                              attributes.get("direction"), attributes["description"], attributes["amount"],
                              attributes.get("reason"), attributes.get("tags"), relationships)

class WirePaymentDTO(BasePayment):
    def __init__(self, id: str, created_at: datetime, status: AchStatus, counterparty: WireCounterparty, direction: str,
                 description: str, amount: int, reason: Optional[str], tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BasePayment.__init__(self, id, created_at, direction, description, amount, reason, tags, relationships)
        self.type = 'wirePayment'
        self.attributes["status"] = status
        self.attributes["counterparty"] = counterparty

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return WirePaymentDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["status"],
                              WireCounterparty.from_json_api(attributes["counterparty"]), attributes["direction"],
                              attributes["description"], attributes["amount"], attributes.get("reason"),
                              attributes.get("tags"), relationships)

PaymentDTO = Union[AchPaymentDTO, BookPaymentDTO, WirePaymentDTO]

class CreatePaymentBaseRequest(UnitRequest):
    def __init__(self, amount: int, description: str, relationships: Dict[str, Relationship],
                 idempotency_key: Optional[str], tags: Optional[Dict[str, str]], direction: str = "Credit",
                 type: str = "achPayment"):
        self.type = type
        self.amount = amount
        self.description = description
        self.direction = direction
        self.idempotency_key = idempotency_key
        self.tags = tags
        self.relationships = relationships

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": self.type,
                "attributes": {
                    "amount": self.amount,
                    "direction": self.direction,
                    "description": self.description
                },
                "relationships": self.relationships
            }
        }

        if self.idempotency_key:
            payload["data"]["attributes"]["idempotencyKey"] = self.idempotency_key

        if self.tags:
            payload["data"]["attributes"]["tags"] = self.tags

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())

class CreateInlinePaymentRequest(CreatePaymentBaseRequest):
    def __init__(self, amount: int, description: str, counterparty: Counterparty, relationships: Dict[str, Relationship],
                 addenda: Optional[str], idempotency_key: Optional[str], tags: Optional[Dict[str, str]],
                 direction: str = "Credit"):
        CreatePaymentBaseRequest.__init__(self, amount, description, relationships, idempotency_key, tags, direction)
        self.counterparty = counterparty
        self.addenda = addenda

    def to_json_api(self) -> Dict:
        payload = CreatePaymentBaseRequest.to_json_api(self)

        payload["data"]["attributes"]["counterparty"] = self.counterparty

        if self.addenda:
            payload["data"]["attributes"]["addenda"] = self.addenda

        return payload

class CreateLinkedPaymentRequest(CreatePaymentBaseRequest):
    def __init__(self, amount: int, description: str, relationships: Dict[str, Relationship], addenda: Optional[str],
                 verify_counterparty_balance: Optional[bool], idempotency_key: Optional[str],
                 tags: Optional[Dict[str, str]], direction: str = "Credit"):
        CreatePaymentBaseRequest.__init__(self, amount, description, relationships, idempotency_key, tags, direction)
        self.addenda = addenda
        self.verify_counterparty_balance = verify_counterparty_balance

    def to_json_api(self) -> Dict:
        payload = CreatePaymentBaseRequest.to_json_api(self)

        if self.addenda:
            payload["data"]["attributes"]["addenda"] = self.addenda

        if self.verify_counterparty_balance:
            payload["data"]["attributes"]["verifyCounterpartyBalance"] = self.verify_counterparty_balance

        return payload

class CreateVerifiedPaymentRequest(CreatePaymentBaseRequest):
    def __init__(self, amount: int, description: str, plaid_processor_token: str, relationships: Dict[str, Relationship],
                 counterparty_name: Optional[str], verify_counterparty_balance: Optional[bool],
                 idempotency_key: Optional[str], tags: Optional[Dict[str, str]], direction: str = "Credit"):
        CreatePaymentBaseRequest.__init__(self, amount, description, relationships, idempotency_key, tags)
        self.plaid_Processor_token = plaid_Processor_token
        self.counterparty_name = counterparty_name
        self.verify_counterparty_balance = verify_counterparty_balance

    def to_json_api(self) -> Dict:
        payload = CreatePaymentBaseRequest.to_json_api(self)
        payload["data"]["attributes"]["counterparty"] = self.counterparty
        payload["data"]["attributes"]["plaidProcessorToken"] = self.plaid_processor_token

        if counterparty_name:
            payload["data"]["attributes"]["counterpartyName"] = self.counterparty_name

        if verify_counterparty_balance:
            payload["data"]["attributes"]["verifyCounterpartyBalance"] = self.verify_counterparty_balance

        return payload

class CreateBookPaymentRequest(CreatePaymentBaseRequest):
    def __init__(self, amount: int, description: str, relationships: Dict[str, Relationship],
                 idempotency_key: Optional[str] = None, tags: Optional[Dict[str, str]] = None,
                 direction: str = "Credit"):
        super().__init__(amount, description, relationships, idempotency_key, tags, direction, "bookPayment")

class CreateWirePaymentRequest(CreatePaymentBaseRequest):
    def __init__(self, amount: int, description: str, counterparty: WireCounterparty,
                 relationships: Dict[str, Relationship], idempotency_key: Optional[str], tags: Optional[Dict[str, str]],
                 direction: str = "Credit"):
        CreatePaymentBaseRequest.__init__(self, amount, description, relationships, idempotency_key, tags, direction,
                                      "wirePayment")
        self.counterparty = counterparty

    def to_json_api(self) -> Dict:
        payload = CreatePaymentBaseRequest.to_json_api(self)
        payload["data"]["attributes"]["counterparty"] = self.counterparty
        return payload

CreatePaymentRequest = Union[CreateInlinePaymentRequest, CreateLinkedPaymentRequest, CreateVerifiedPaymentRequest,
                             CreateBookPaymentRequest, CreateWirePaymentRequest]

class PatchAchPaymentRequest(object):
    def __init__(self, payment_id: str, tags: Dict[str, str]):
        self.payment_id = payment_id
        self.tags = tags

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "achPayment",
                "attributes": {
                    "tags": self.tags
                }
            }
        }

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())

class PatchBookPaymentRequest(object):
    def __init__(self, payment_id: str, tags: Dict[str, str]):
        self.payment_id = payment_id
        self.tags = tags

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "bookPayment",
                "attributes": {
                    "tags": self.tags
                }
            }
        }

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())

PatchPaymentRequest = Union[PatchAchPaymentRequest, PatchBookPaymentRequest]

class ListPaymentParams(UnitParams):
    def __init__(self, limit: int = 100, offset: int = 0, account_id: Optional[str] = None,
                 customer_id: Optional[str] = None, tags: Optional[object] = None,
                 status: Optional[List[AchStatus]] = None, type: Optional[List[PaymentTypes]] = None,
                 direction: Optional[List[PaymentDirections]] = None, since: Optional[str] = None,
                 until: Optional[str] = None, sort: Optional[Literal["createdAt", "-createdAt"]] = None,
                 include: Optional[str] = None):
        self.limit = limit
        self.offset = offset
        self.account_id = account_id
        self.customer_id = customer_id
        self.tags = tags
        self.status = status
        self.type = type
        self.direction = direction
        self.since = since
        self.until = until
        self.sort = sort
        self.include = include

    def to_dict(self) -> Dict:
        parameters = {"page[limit]": self.limit, "page[offset]": self.offset}
        if self.customer_id:
            parameters["filter[customerId]"] = self.customer_id
        if self.account_id:
            parameters["filter[accountId]"] = self.account_id
        if self.tags:
            parameters["filter[tags]"] = self.tags
        if self.status:
            for idx, status_filter in enumerate(self.status):
                parameters[f"filter[status][{idx}]"] = status_filter
        if self.type:
            for idx, type_filter in enumerate(self.type):
                parameters[f"filter[type][{idx}]"] = type_filter
        if self.direction:
            for idx, direction_filter in enumerate(self.direction):
                parameters[f"filter[direction][{idx}]"] = direction_filter
        if self.since:
            parameters["filter[since]"] = self.since
        if self.until:
            parameters["filter[until]"] = self.until
        if self.sort:
            parameters["sort"] = self.sort
        if self.include:
            parameters["include"] = self.include
        return parameters

