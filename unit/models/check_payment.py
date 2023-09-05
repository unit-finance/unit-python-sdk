from unit.models import *
from unit.utils import date_utils

CheckPaymentStatus = Literal["New", "Pending", "Canceled", "InDelivery", "Delivered", "ReturnedToSender", "Processed",
                             "PendingReview", "MarkedForReturn", "Returned"]

CheckPaymentReturnReason = Literal["NotSufficientFunds", "UncollectedFundsHold", "StopPayment", "ClosedAccount",
                                   "UnableToLocateAccount", "FrozenOrBlockedAccount", "StaleDated", "PostDated",
                                   "NotValidCheckOrCashItem", "AlteredOrFictitious","UnableToProcess",
                                   "ItemExceedsDollarLimit", "NotAuthorized", "ReferToMaker", "UnusableImage",
                                   "DuplicatePresentment", "WarrantyBreach", "UnauthorizedWarrantyBreach"]

CheckPaymentDeliveryStatus = Literal["Mailed", "InLocalArea", "Delivered", "Rerouted", "ReturnedToSender"]

AdditionalVerificationStatus = Literal["Required", "NotRequired", "Approved"]

CheckPaymentPendingReviewReasons = Literal["SoftLimit"]


class CheckPaymentCounterparty(UnitDTO):
    def __init__(self, name: str, address: Optional[Address] = None, counterparty_moved: Optional[bool] = None):
        self.name = name
        self.address = address
        self.counterparty_moved = counterparty_moved

    @staticmethod
    def from_json_api(j):
        if not j:
            return None

        return CheckPaymentCounterparty(j["name"], j.get("address"), j.get("counterpartyMoved"))


class CheckPaymentDTO(UnitDTO):
    def __init__(self, _id: str, _type: str, created_at: datetime, updated_at: datetime, status: CheckPaymentStatus,
                 amount: int, description: str, check_number: str, originated: bool, expected_delivery: str,
                 relationships: Dict[str, object], on_us: Optional[str] = None, on_us_auxiliary: Optional[str] = None,
                 counterparty_routing_number: Optional[str] = None,
                 counterparty: Optional[CheckPaymentCounterparty] = None,
                 return_status_reason: Optional[CheckPaymentReturnReason] = None, reject_reason: Optional[str] = None,
                 pending_review_reasons: Optional[List[CheckPaymentPendingReviewReasons]] = None,
                 return_cutoff_time: Optional[date] = None,
                 additional_verification_status: Optional[AdditionalVerificationStatus] = None,
                 delivery_status: Optional[CheckPaymentDeliveryStatus] = None, tracked_at: Optional[datetime] = None,
                 postal_code: Optional[str] = None, expiration_date: Optional[str] = None,
                 send_at: Optional[datetime] = None, memo: Optional[str] = None, tags: Optional[Dict[str, str]] = None):
        self.id = _id
        self.type = _type
        self.attributes = {"createdAt": created_at, "updatedAt": updated_at, "status": status, "amount": amount,
                           "description": description, "checkNumber": check_number, "originated": originated,
                           "onUs": on_us, "onUsAuxiliary": on_us_auxiliary,
                           "counterpartyRoutingNumber": counterparty_routing_number,
                           "returnStatusReason": return_status_reason, "rejectReason": reject_reason,
                           "pendingReviewReasons": pending_review_reasons, "returnCutoffTime": return_cutoff_time,
                           "additionalVerificationStatus": additional_verification_status, "sendAt": send_at,
                           "counterparty": counterparty, "memo": memo,
                           "tags": tags, "deliveryStatus": delivery_status, "trackedAt": tracked_at,
                           "postalCode": postal_code, "expirationDate": expiration_date,
                           "expectedDelivery": expected_delivery}
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id: str, _type: str, attributes: Dict[str, object], relationships: Dict[str, str]):
        return CheckPaymentDTO(_id, _type, date_utils.to_datetime(attributes["createdAt"]),
                               date_utils.to_datetime(attributes["updatedAt"]), attributes["status"],
                               attributes["amount"], attributes["description"], attributes["checkNumber"],
                               attributes.get("originated"), attributes.get("expectedDelivery"), relationships,
                               attributes.get("onUs"), attributes.get("onUsAuxiliary"),
                               attributes.get("counterpartyRoutingNumber"),
                               CheckPaymentCounterparty.from_json_api(attributes.get("counterparty")),
                               attributes.get("returnStatusReason"), attributes.get("rejectReason"),
                               attributes.get("pendingReviewReasons"),
                               date_utils.to_datetime(attributes.get("returnCutoffTime")),
                               attributes.get("additionalVerificationStatus"), attributes.get("deliveryStatus"),
                               date_utils.to_datetime(attributes.get("trackedAt")),
                               attributes.get("postalCode"), attributes.get("expirationDate"),
                               date_utils.to_datetime(attributes.get("sendAt")), attributes.get("memo"),
                               attributes.get("tags"))


class CreateCheckPaymentRequest(UnitRequest):
    def __init__(self, amount: int, counterparty: CheckPaymentCounterparty, description: str,
                 relationships: Dict[str, Relationship], memo: Optional[str] = None, send_date: Optional[str] = None,
                 idempotency_key: Optional[str] = None, tags: Tags = None):
        self.amount = amount
        self.counterparty = counterparty
        self.description = description
        self.memo = memo
        self.send_date = send_date
        self.idempotency_key = idempotency_key
        self.tags = tags
        self.relationships = relationships

    def to_json_api(self) -> Dict:
        return super().to_payload("checkPayment")

    def __repr__(self):
        return json.dumps(self.to_json_api())


class ListCheckPaymentParams(UnitParams):
    def __init__(self, offset: int = 0, limit: int = 100, customer_id: Optional[str] = None,
                 account_id: Optional[str] = None, tags: Optional[Dict[str, str]] = None,
                 sort: Optional[Literal["createdAt", "-createdAt"]] = None, since: Optional[str] = None,
                 until: Optional[str] = None, status: Optional[List[CheckPaymentStatus]] = None,
                 from_amount: Optional[int] = None, to_amount: Optional[int] = None, check_number: Optional[int] = None,
                 include: Optional[str] = None):
        self.offset = offset
        self.limit = limit
        self.account_id = account_id
        self.customer_id = customer_id
        self.sort = sort
        self.tags = tags
        self.since = since
        self.until = until
        self.include = include
        self.status = status
        self.from_amount = from_amount
        self.to_amount = to_amount
        self.check_number = check_number

    def to_dict(self) -> Dict:
        parameters = {"page[limit]": self.limit, "page[offset]": self.offset}
        if self.account_id:
            parameters["filter[accountId]"] = self.account_id
        if self.customer_id:
            parameters["filter[customerId]"] = self.customer_id
        if self.tags:
            parameters["filter[tags]"] = json.dumps(self.tags)
        if self.sort:
            parameters["sort"] = self.sort
        if self.include:
            parameters["include"] = self.include
        if self.since:
            parameters["filter[since]"] = self.since
        if self.until:
            parameters["filter[until]"] = self.until
        if self.from_amount:
            parameters["filter[fromAmount]"] = self.from_amount
        if self.to_amount:
            parameters["filter[toAmount]"] = self.to_amount
        if self.check_number:
            parameters["filter[checkNumber]"] = self.check_number
        if self.status:
            for idx, status_filter in enumerate(self.status):
                parameters[f"filter[status][{idx}]"] = status_filter
        return parameters


class ReturnCheckPaymentRequest(UnitRequest):
    def __init__(self, reason: CheckPaymentReturnReason):
        self.reason = reason

    def to_payload(self):
        super().to_payload("checkPaymentReturn")

    def __repr__(self):
        return json.dumps(self.to_json_api())


class ApproveCheckPaymentRequest(UnitRequest):
    def to_payload(self):
        super().to_payload("additionalVerification")

