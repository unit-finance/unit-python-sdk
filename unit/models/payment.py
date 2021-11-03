from unit.utils import date_utils
from unit.models import *

AchStatus = Literal["Pending", "Rejected", "Clearing", "Sent", "Canceled", "Returned"]

class BasePayment(object):
    def __init__(self, id: str, created_at: datetime, direction: str, description: str, amount: int,
                 reason: Optional[str], tags: Optional[dict[str, str]],
                 relationships: Optional[dict[str, Relationship]]):
        self.id = id
        self.attributes = {"createdAt": created_at, "direction": direction, "description": description,
                           "amount": amount, "reason": reason, "tags": tags}
        self.relationships = relationships


class AchPaymentDTO(BasePayment):
    def __init__(self, id: str, created_at: datetime, status: AchStatus, counterparty: Counterparty, direction: str,
                 description: str, amount: int, addenda: Optional[str], reason: Optional[str],
                 settlement_date: Optional[datetime], tags: Optional[dict[str, str]],
                 relationships: Optional[dict[str, Relationship]]):
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
                 reason: Optional[str], tags: Optional[dict[str, str]],
                 relationships: Optional[dict[str, Relationship]]):
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
                 description: str, amount: int, reason: Optional[str], tags: Optional[dict[str, str]],
                 relationships: Optional[dict[str, Relationship]]):
        BasePayment.__init__(self, id, created_at, direction, description, amount, reason, tags, relationships)
        self.type = 'wirePayment'
        self.attributes["status"] = status
        self.attributes["counterparty"] = counterparty
        self.attributes["addenda"] = addenda
        self.attributes["settlementDate"] = settlement_date

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return WirePaymentDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["status"],
                              WireCounterparty.from_json_api(attributes["counterparty"]), attributes["direction"],
                              attributes["description"], attributes["amount"], attributes.get("reason"),
                              attributes.get("tags"), relationships)

PaymentDTO = Union[AchPaymentDTO, BookPaymentDTO, WirePaymentDTO]

class CreatePaymentRequest(object):
    def __init__(self, amount: int, description: str, relationships: dict[str, Relationship],
                 idempotency_key: Optional[str], tags: Optional[dict[str, str]], direction: str = "Credit",
                 type: str = "achPayment"):
        self.type = type
        self.amount = amount
        self.description = description
        self.direction = direction
        self.idempotency_key = idempotency_key
        self.tags = tags
        self.relationships = relationships

    def to_json_api(self) -> dict:
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

class CreateInlinePaymentRequest(CreatePaymentRequest):
    def __init__(self, amount: int, description: str, counterparty: Counterparty, relationships: dict[str, Relationship],
                 addenda: Optional[str], idempotency_key: Optional[str], tags: Optional[dict[str, str]],
                 direction: str = "Credit"):
        CreatePaymentRequest.__init__(self, amount, description, relationships, idempotency_key, tags, direction)
        self.counterparty = counterparty
        self.addenda = addenda

    def to_json_api(self) -> dict:
        payload = CreatePaymentRequest.to_json_api(self)
        payload["data"]["attributes"]["counterparty"] = self.counterparty

        if self.addenda:
            payload["data"]["attributes"]["addenda"] = self.addenda

        return payload

class CreateLinkedPaymentRequest(CreatePaymentRequest):
    def __init__(self, amount: int, description: str, relationships: dict[str, Relationship], addenda: Optional[str],
                 verify_counterparty_balance: Optional[bool], idempotency_key: Optional[str],
                 tags: Optional[dict[str, str]], direction: str = "Credit"):
        CreatePaymentRequest.__init__(self, amount, description, relationships, idempotency_key, tags, direction)
        self.addenda = addenda
        self.verify_counterparty_balance = verify_counterparty_balance

    def to_json_api(self) -> dict:
        payload = CreatePaymentRequest.to_json_api(self)

        if self.addenda:
            payload["data"]["attributes"]["addenda"] = self.addenda

        if self.verify_counterparty_balance:
            payload["data"]["attributes"]["verifyCounterpartyBalance"] = self.verify_counterparty_balance

        return payload

class CreateVerifiedPaymentRequest(CreatePaymentRequest):
    def __init__(self, amount: int, description: str, plaid_processor_token: str, relationships: dict[str, Relationship],
                 counterparty_name: Optional[str], verify_counterparty_balance: Optional[bool],
                 idempotency_key: Optional[str], tags: Optional[dict[str, str]], direction: str = "Credit"):
        CreatePaymentRequest.__init__(self, amount, description, relationships, idempotency_key, tags)
        self.plaid_Processor_token = plaid_Processor_token
        self.counterparty_name = counterparty_name
        self.verify_counterparty_balance = verify_counterparty_balance

    def to_json_api(self) -> dict:
        payload = CreatePaymentRequest.to_json_api(self)
        payload["data"]["attributes"]["counterparty"] = self.counterparty
        payload["data"]["attributes"]["plaidProcessorToken"] = self.plaid_processor_token

        if counterparty_name:
            payload["data"]["attributes"]["counterpartyName"] = self.counterparty_name

        if verify_counterparty_balance:
            payload["data"]["attributes"]["verifyCounterpartyBalance"] = self.verify_counterparty_balance


        return payload

class CreateBookPaymentRequest(CreatePaymentRequest):
    def __init__(self, amount: int, description: str, relationships: dict[str, Relationship],
                 idempotency_key: Optional[str] = None, tags: Optional[dict[str, str]] = None,
                 direction: str = "Credit"):
        super().__init__(amount, description, relationships, idempotency_key, tags, direction, "bookPayment")

class CreateWirePaymentRequest(CreatePaymentRequest):
    def __init__(self, amount: int, description: str, counterparty: WireCounterparty,
                 relationships: dict[str, Relationship], idempotency_key: Optional[str], tags: Optional[dict[str, str]],
                 direction: str = "Credit"):
        CreatePaymentRequest.__init__(self, amount, description, relationships, idempotency_key, tags, direction,
                                      "wirePayment")
        self.counterparty = counterparty

    def to_json_api(self) -> dict:
        payload = CreatePaymentRequest.to_json_api(self)
        payload["data"]["attributes"]["counterparty"] = self.counterparty
        return payload

CreatePaymentRequest = Union[CreateInlinePaymentRequest, CreateLinkedPaymentRequest, CreateVerifiedPaymentRequest,
                             CreateBookPaymentRequest, CreateWirePaymentRequest]

class PatchAchPaymentRequest(object):
    def __init__(self, payment_id: str, tags: dict[str, str]):
        self.payment_id = payment_id
        self.tags = tags

    def to_json_api(self) -> dict:
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
    def __init__(self, payment_id: str, tags: dict[str, str]):
        self.payment_id = payment_id
        self.tags = tags

    def to_json_api(self) -> dict:
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