from unit.utils import date_utils
from unit.models import *
from unit.models.check_payment import CheckPaymentCounterparty

PaymentTypes = Literal["AchPayment", "BookPayment", "WirePayment"]
PaymentDirections = Literal["Debit", "Credit"]
PaymentStatus = Literal["Pending", "Rejected", "Clearing", "Sent", "Canceled", "Returned"]
RecurringStatus = Literal["Active", "Completed", "Disabled"]
DayOfWeek = Literal["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


class Schedule(UnitDTO):
    def __init__(self, start_time: datetime, end_time: datetime, day_of_month: int, day_of_week: DayOfWeek,
                 interval: str, next_scheduled_action: str, total_number_of_payments: int):
        self.start_time = start_time
        self.end_time = end_time
        self.day_of_month = day_of_month
        self.day_of_week = day_of_week
        self.interval = interval
        self.next_scheduled_action = next_scheduled_action
        self.total_number_of_payments = total_number_of_payments

    @staticmethod
    def from_json_api(data: Dict):
        return Schedule(date_utils.to_date(data["startTime"]), date_utils.to_date(data.get("endTime")),
                        data.get("dayOfMonth"), data.get("dayOfWeek"), data["interval"], data["nextScheduledAction"],
                        data.get("totalNumberOfPayments"))


class CreateSchedule(UnitDTO):
    def __init__(self, interval: str, day_of_month: int, start_time: Optional[datetime] = None,
                 end_time: Optional[datetime] = None, day_of_week: Optional[DayOfWeek] = None,
                 total_number_of_payments: Optional[int] = None):
        self.start_time = start_time
        self.end_time = end_time
        self.day_of_month = day_of_month
        self.day_of_week = day_of_week
        self.interval = interval
        self.total_number_of_payments = total_number_of_payments


class BasePayment(object):
    def __init__(self, _id: str, created_at: datetime, status: PaymentStatus, direction: PaymentDirections, description: str,
                 amount: int, reason: Optional[str], tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        self.id = _id
        self.attributes = {"createdAt": created_at, "status": status, "direction": direction,
                           "description": description, "amount": amount, "reason": reason, "tags": tags}
        self.relationships = relationships


class AchPaymentDTO(BasePayment):
    def __init__(self, _id: str, created_at: datetime, status: PaymentStatus, counterparty: Counterparty, direction: str,
                 description: str, amount: int, addenda: Optional[str], reason: Optional[str],
                 settlement_date: Optional[date], tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]], same_day: bool):
        BasePayment.__init__(self, _id, created_at, status, direction, description, amount, reason, tags, relationships)
        self.type = 'achPayment'
        self.attributes["counterparty"] = counterparty
        self.attributes["addenda"] = addenda
        self.attributes["settlementDate"] = settlement_date
        self.attributes["sameDay"] = same_day

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AchPaymentDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["status"],
                             Counterparty.from_json_api(attributes["counterparty"]), attributes["direction"], attributes["description"],
                             attributes["amount"], attributes.get("addenda"), attributes.get("reason"),
                             date_utils.to_date(attributes.get("settlementDate")), attributes.get("tags"), relationships,
                             attributes["sameDay"])


class BookPaymentDTO(BasePayment):
    def __init__(self, _id: str, created_at: datetime, status: PaymentStatus, direction: Optional[str], description: str,
                 amount: int, reason: Optional[str], tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BasePayment.__init__(self, _id, created_at, status, direction, description, amount, reason, tags, relationships)
        self.type = 'bookPayment'

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return BookPaymentDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["status"],
                              attributes.get("direction"), attributes["description"], attributes["amount"],
                              attributes.get("reason"), attributes.get("tags"), relationships)


class WirePaymentDTO(BasePayment):
    def __init__(self, _id: str, created_at: datetime, status: PaymentStatus, counterparty: WireCounterparty,
                 direction: str, description: str, amount: int, reason: Optional[str], tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BasePayment.__init__(self, _id, created_at, status, direction, description, amount, reason, tags, relationships)
        self.type = "wirePayment"
        self.attributes["counterparty"] = counterparty

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return WirePaymentDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["status"],
                              WireCounterparty.from_json_api(attributes["counterparty"]), attributes["direction"],
                              attributes["description"], attributes["amount"], attributes.get("reason"),
                              attributes.get("tags"), relationships)

PaymentDTO = Union[AchPaymentDTO, BookPaymentDTO, WirePaymentDTO]

AchReceivedPaymentStatus = Literal["Pending", "Advanced", "Completed", "Returned"]


class AchReceivedPaymentDTO(object):
    def __init__(self, _id: str, created_at: datetime, status: AchReceivedPaymentStatus, was_advanced: bool,
                 is_advanceable: bool, direction: str, completion_date: date, return_reason: Optional[str], amount: int, description: str,
                 addenda: Optional[str], company_name: str, counterparty_routing_number: str, trace_number: str,
                 sec_code: Optional[str], tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        self.id = _id
        self.type = "achReceivedPayment"
        self.attributes = {"createdAt": created_at, "status": status, "wasAdvanced": was_advanced,
                           "isAdvanceable": is_advanceable, "direction": direction, "completionDate": completion_date, "returnReason": return_reason, "description": description,
                           "amount": amount, "addenda": addenda, "companyName": company_name,
                           "counterpartyRoutingNumber": counterparty_routing_number, "traceNumber": trace_number,
                           "secCode": sec_code, "tags": tags}
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AchReceivedPaymentDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["status"],
                                     attributes["wasAdvanced"], attributes.get("isAdvanceable"), attributes["direction"], date_utils.to_date(attributes["completionDate"]),
                                     attributes.get("returnReason"), attributes["amount"], attributes["description"],
                                     attributes.get("addenda"), attributes.get("companyName"),
                                     attributes.get("counterpartyRoutingNumber"), attributes.get("traceNumber"),
                                     attributes.get("secCode"), attributes.get("tags"), relationships)


class BaseRecurringPaymentDTO(object):
    def __init__(self, _id: str, _type: str, created_at: datetime, update_at: datetime, amount: int, description: str,
                 addenda: Optional[str], status: RecurringStatus, number_of_payments: int, schedule: Schedule,
                 tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        self.id = _id
        self.type = _type
        self.attributes = {"createdAt": created_at, "updatedAt": update_at, "amount": amount,
                           "description": description, "addenda": addenda, "status": status,
                           "numberOfPayments": number_of_payments, "schedule": schedule, "tags": tags}
        self.relationships = relationships


class RecurringCreditAchPaymentDTO(BaseRecurringPaymentDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return RecurringCreditAchPaymentDTO(_id, _type, date_utils.to_datetime(attributes["createdAt"]),
                                            date_utils.to_datetime(attributes["updatedAt"]), attributes["amount"],
                                            attributes["description"], attributes.get("addenda"), attributes["status"],
                                            attributes["numberOfPayments"],
                                            Schedule.from_json_api(attributes["schedule"]), attributes.get("tags"),
                                            relationships)


class RecurringCreditBookPaymentDTO(BaseRecurringPaymentDTO):
    def __init__(self, _id: str, _type: str, created_at: datetime, update_at: datetime, amount: int, description: str,
                 addenda: Optional[str], status: RecurringStatus, number_of_payments: int, schedule: Schedule,
                 transaction_summary_override: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        super().__init__(_id, _type, created_at, update_at, amount, description, addenda, status, number_of_payments,
                         schedule, tags, relationships)
        self.attributes["transactionSummaryOverride"] = transaction_summary_override

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return RecurringCreditBookPaymentDTO(_id, _type, date_utils.to_datetime(attributes["createdAt"]),
                                             date_utils.to_datetime(attributes["updatedAt"]), attributes["amount"],
                                             attributes["description"], attributes.get("addenda"), attributes["status"],
                                             attributes["numberOfPayments"],
                                             Schedule.from_json_api(attributes["schedule"]),
                                             attributes.get("transactionSummaryOverride"), attributes.get("tags"),
                                             relationships)


class RecurringDebitAchPaymentDTO(BaseRecurringPaymentDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return RecurringDebitAchPaymentDTO(_id, _type, date_utils.to_datetime(attributes["createdAt"]),
                                           date_utils.to_datetime(attributes["updatedAt"]), attributes["amount"],
                                           attributes["description"], attributes.get("addenda"), attributes["status"],
                                           attributes["numberOfPayments"],
                                           Schedule.from_json_api(attributes["schedule"]), attributes.get("tags"),
                                           relationships)


RecurringPaymentDTO = Union[RecurringCreditAchPaymentDTO, RecurringDebitAchPaymentDTO, RecurringCreditBookPaymentDTO]


class BulkPaymentsDTO(UnitDTO):
    def __init__(self, _type: str, bulk_id: str):
        self.type = _type
        self.attributes = {"bulkId": bulk_id}

    @staticmethod
    def from_json_api(_type, attributes):
        return BulkPaymentsDTO(_type, attributes.get("bulkId"))


class CreateRecurringPaymentBaseRequest(UnitRequest):
    def __init__(self,_type: str, amount: int, description: str, schedule: CreateSchedule, relationships: Dict[str, Relationship],
                 idempotency_key: Optional[str], tags: Optional[Dict[str, str]]):
        self.type = _type
        self.amount = amount
        self.description = description
        self.schedule = schedule
        self.idempotency_key = idempotency_key
        self.tags = tags
        self.relationships = relationships

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": self.type,
                "attributes": {
                    "amount": self.amount,
                    "description": self.description,
                    "schedule": self.schedule
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


class CreateRecurringCreditAchPaymentRequest(CreateRecurringPaymentBaseRequest):
    def __init__(self, amount: int, description: str, schedule: CreateSchedule, relationships: Dict[str, Relationship],
                 addenda: Optional[str] = None, idempotency_key: Optional[str] = None,
                 tags: Optional[Dict[str, str]] = None):
        CreateRecurringPaymentBaseRequest.__init__(self, "recurringCreditAchPayment", amount, description, schedule,
                                                   relationships, idempotency_key, tags)
        self.addenda = addenda

    def to_json_api(self) -> Dict:
        payload = CreateRecurringPaymentBaseRequest.to_json_api(self)

        if self.addenda:
            payload["data"]["attributes"]["addenda"] = self.addenda

        return payload


class CreateRecurringCreditBookPaymentRequest(CreateRecurringPaymentBaseRequest):
    def __init__(self, amount: int, description: str, schedule: CreateSchedule, relationships: Dict[str, Relationship],
                 transaction_summary_override: Optional[str] = None, idempotency_key: Optional[str] = None,
                 tags: Optional[Dict[str, str]] = None):
        CreateRecurringPaymentBaseRequest.__init__(self, "recurringCreditBookPayment", amount, description, schedule,
                                                   relationships, idempotency_key, tags)
        self.transaction_summary_override = transaction_summary_override

    def to_json_api(self) -> Dict:
        payload = CreateRecurringPaymentBaseRequest.to_json_api(self)

        if self.transaction_summary_override:
            payload["data"]["attributes"]["transactionSummaryOverride"] = self.transaction_summary_override

        return payload


class CreateRecurringDebitAchPaymentRequest(CreateRecurringPaymentBaseRequest):
    def __init__(self, amount: int, description: str, schedule: CreateSchedule, relationships: Dict[str, Relationship],
                 addenda: Optional[str] = None, idempotency_key: Optional[str] = None,
                 tags: Optional[Dict[str, str]] = None, verify_counterparty_balance: Optional[bool] = False,
                 same_day: Optional[bool] = False):
        CreateRecurringPaymentBaseRequest.__init__(self, "recurringDebitAchPayment", amount, description, schedule,
                                                   relationships, idempotency_key, tags)
        self.addenda = addenda
        self.verify_counterparty_balance = verify_counterparty_balance
        self.same_day = same_day

    def to_json_api(self) -> Dict:
        payload = CreateRecurringPaymentBaseRequest.to_json_api(self)

        if self.addenda:
            payload["data"]["attributes"]["addenda"] = self.addenda

        if self.verify_counterparty_balance:
            payload["data"]["attributes"]["verifyCounterpartyBalance"] = self.verify_counterparty_balance

        if self.same_day:
            payload["data"]["attributes"]["sameDay"] = self.same_day

        return payload


CreateRecurringPaymentRequest = Union[CreateRecurringCreditAchPaymentRequest,
                                      CreateRecurringCreditBookPaymentRequest, CreateRecurringDebitAchPaymentRequest]


class CreatePaymentBaseRequest(UnitRequest):
    def __init__(self, amount: int, description: str, relationships: Dict[str, Relationship],
                 idempotency_key: Optional[str] = None, tags: Optional[Dict[str, str]] = None,
                 direction: str = "Credit", addenda: Optional[str] = None, same_day: Optional[bool] = False,
                 sec_code: Optional[str] = None, clearing_days_override: Optional[int] = None,
                 _type: str = "achPayment"):
        self.type = _type
        self.amount = amount
        self.addenda = addenda
        self.same_day = same_day
        self.sec_code = sec_code
        self.clearing_days_override = clearing_days_override
        self.description = description
        self.direction = direction
        self.idempotency_key = idempotency_key
        self.tags = tags
        self.relationships = relationships

    def to_json_api(self, wrap_with_data=True) -> Dict:
        payload = super().to_payload(self.type, self.relationships, ['type'])

        return payload if wrap_with_data else payload.get("data")

    def __repr__(self):
        return json.dumps(self.to_json_api())

class PushToCardPaymentDTO(BasePayment):
    def __init__(self, id: str, created_at: datetime, status: PaymentStatus, direction: Optional[str], description: str,
                 amount: int, astra_routine_id: str, reason: Optional[str], tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BasePayment.__init__(self, id, created_at, status, direction, description, amount, reason, tags, relationships, astra_routine_id)
        self.type = 'pushToCardPayment'

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return PushToCardPaymentDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["status"],
                                    attributes.get("direction"), attributes["description"], attributes["amount"],
                                    attributes["astraRoutineId"], attributes.get("reason"), attributes.get("tags"),
                                    relationships)
class CreateInlinePaymentRequest(CreatePaymentBaseRequest):
    def __init__(self, amount: int, description: str, counterparty: Counterparty, relationships: Dict[str, Relationship],
                 addenda: Optional[str] = None, idempotency_key: Optional[str] = None,
                 tags: Optional[Dict[str, str]] = None, direction: Optional[str] = "Credit",
                 same_day: Optional[bool] = False, sec_code: Optional[str] = None,
                 clearing_days_override: Optional[int] = None):
        CreatePaymentBaseRequest.__init__(self, amount, description, relationships, idempotency_key, tags, direction,
                                          addenda, same_day, sec_code, clearing_days_override)
        self.counterparty = counterparty

    def to_json_api(self) -> Dict:
        payload = CreatePaymentBaseRequest.to_json_api(self)

        payload["data"]["attributes"]["counterparty"] = self.counterparty

        return payload


class CreateLinkedPaymentRequest(CreatePaymentBaseRequest):
    def __init__(self, amount: int, description: str, relationships: Dict[str, Relationship],
                 addenda: Optional[str] = None, verify_counterparty_balance: Optional[bool] = None,
                 idempotency_key: Optional[str] = None, tags: Optional[Dict[str, str]] = None,
                 direction: Optional[str] = "Credit", same_day: Optional[bool] = False, sec_code: Optional[str] = None,
                 clearing_days_override: Optional[int] = None):
        CreatePaymentBaseRequest.__init__(self, amount, description, relationships, idempotency_key, tags, direction,
                                          addenda, same_day, sec_code, clearing_days_override)
        self.verify_counterparty_balance = verify_counterparty_balance

    def to_json_api(self) -> Dict:
        payload = CreatePaymentBaseRequest.to_json_api(self)

        if self.verify_counterparty_balance:
            payload["data"]["attributes"]["verifyCounterpartyBalance"] = self.verify_counterparty_balance

        return payload


class CreateVerifiedPaymentRequest(CreatePaymentBaseRequest):
    def __init__(self, amount: int, description: str, plaid_processor_token: str, relationships: Dict[str, Relationship],
                 counterparty_name: Optional[str] = None, verify_counterparty_balance: Optional[bool] = None,
                 idempotency_key: Optional[str] = None, tags: Optional[Dict[str, str]] = None,
                 direction: str = "Credit", same_day: Optional[bool] = False, addenda: Optional[str] = None,
                 sec_code: Optional[str] = None, clearing_days_override: Optional[int] = None):
        CreatePaymentBaseRequest.__init__(self, amount, description, relationships, idempotency_key, tags,direction,
                                          addenda, same_day, sec_code, clearing_days_override)
        self.plaid_processor_token = plaid_processor_token
        self.counterparty_name = counterparty_name
        self.verify_counterparty_balance = verify_counterparty_balance

    def to_json_api(self) -> Dict:
        payload = CreatePaymentBaseRequest.to_json_api(self)
        payload["data"]["attributes"]["plaidProcessorToken"] = self.plaid_processor_token

        if self.counterparty_name:
            payload["data"]["attributes"]["counterpartyName"] = self.counterparty_name

        if self.verify_counterparty_balance:
            payload["data"]["attributes"]["verifyCounterpartyBalance"] = self.verify_counterparty_balance

        return payload


class CreateBookPaymentRequest(CreatePaymentBaseRequest):
    def __init__(self, amount: int, description: str, relationships: Dict[str, Relationship],
                 idempotency_key: Optional[str] = None, tags: Optional[Dict[str, str]] = None,
                 direction: str = "Credit"):
        super().__init__(amount, description, relationships, idempotency_key, tags, direction, _type="bookPayment")


class CreateWirePaymentRequest(CreatePaymentBaseRequest):
    def __init__(self, amount: int, description: str, counterparty: WireCounterparty,
                 relationships: Dict[str, Relationship], idempotency_key: Optional[str] = None,
                 tags: Optional[Dict[str, str]] = None, direction: str = "Credit"):
        CreatePaymentBaseRequest.__init__(self, amount, description, relationships, idempotency_key, tags, direction,
                                          _type="wirePayment")
        self.counterparty = counterparty

    def to_json_api(self) -> Dict:
        payload = CreatePaymentBaseRequest.to_json_api(self)
        payload["data"]["attributes"]["counterparty"] = self.counterparty
        return payload

class CreatePushToCardPaymentRequest(CreatePaymentBaseRequest):
        def __init__(self, amount: int, description: str, configuration: dict,
                     relationships: Dict[str, Relationship],
                     idempotency_key: Optional[str] = None, tags: Optional[Dict[str, str]] = None):
            CreatePaymentBaseRequest.__init__(amount, description, relationships, idempotency_key, tags,_type="pushToCardPayment")
            self.configuration = configuration
        def to_json_api(self) -> Dict:
            payload = CreatePaymentBaseRequest.to_json_api(self)
            return payload

class CreateCheckPaymentRequest(CreatePaymentBaseRequest):
        def __init__(
                self,
                description: str,
                amount: int,
                counterparty: CheckPaymentCounterparty,
                idempotency_key: str,
                relationships: Dict[str, Relationship],
                memo: Optional[str] = None,
                send_date: Optional[str] = None,
                tags: Optional[Dict[str, str]] = None,
        ):
            CreatePaymentBaseRequest.__init__(self, amount, description, relationships, idempotency_key, tags,
                                             _type="checkPayment")
            self.send_date = send_date
            self.counterparty = counterparty
            self.memo = memo

        def to_json_api(self) -> Dict:
            payload = CreatePaymentBaseRequest.to_json_api(self)
            payload["data"]["attributes"]["counterparty"]["name"] = self.counterparty.name
            payload["data"]["attributes"]["counterparty"]["counterpartyMoved"] = self.counterparty.counterparty_moved
            payload["data"]["attributes"]["counterparty"]["address"] = self.counterparty.address
            return payload



CreatePaymentRequest = Union[CreateInlinePaymentRequest, CreateLinkedPaymentRequest, CreateVerifiedPaymentRequest,
                             CreateBookPaymentRequest, CreateWirePaymentRequest, CreatePushToCardPaymentRequest, CreateCheckPaymentRequest]


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
        return json.dumps(self.to_json_api())


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
        return json.dumps(self.to_json_api())


PatchPaymentRequest = Union[PatchAchPaymentRequest, PatchBookPaymentRequest]


class ListPaymentParams(UnitParams):
    def __init__(self, limit: int = 100, offset: int = 0, account_id: Optional[str] = None,
                 customer_id: Optional[str] = None, tags: Optional[Dict[str, str]] = None,
                 status: Optional[List[PaymentStatus]] = None, type: Optional[List[PaymentTypes]] = None,
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
            parameters["filter[tags]"] = json.dumps(self.tags)
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


class ListRecurringPaymentParams(UnitParams):
    def __init__(self, limit: int = 100, offset: int = 0, account_id: Optional[str] = None,
                 customer_id: Optional[str] = None, tags: Optional[object] = None,
                 status: Optional[List[AchReceivedPaymentStatus]] = None,
                 _type: Optional[List[str]] = None, from_start_time: Optional[str] = None,
                 to_start_time: Optional[str] = None,  from_end_time: Optional[str] = None,
                 to_end_time: Optional[str] = None, sort: Optional[Literal["createdAt", "-createdAt"]] = None):
        self.limit = limit
        self.offset = offset
        self.account_id = account_id
        self.customer_id = customer_id
        self.tags = tags
        self.status = status
        self._type = _type
        self.from_start_time = from_start_time
        self.to_start_time = to_start_time
        self.from_end_time = from_end_time
        self.to_end_time = to_end_time
        self.sort = sort

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
        if self._type:
            for idx, type_filter in enumerate(self._type):
                parameters[f"filter[type][{idx}]"] = type_filter
        if self.from_start_time:
            parameters["filter[fromStartTime]"] = self.from_start_time
        if self.to_start_time:
            parameters["filter[toStartTime]"] = self.to_start_time
        if self.from_end_time:
            parameters["filter[fromEndTime]"] = self.from_end_time
        if self.to_end_time:
            parameters["filter[toEndTime]"] = self.to_end_time
        if self.sort:
            parameters["sort"] = self.sort
        return parameters
