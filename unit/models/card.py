from unit.utils import date_utils
from unit.models import *

CardStatus = Literal["Inactive", "Active", "Stolen", "Lost", "Frozen", "ClosedByCustomer", "SuspectedFraud"]


class IndividualDebitCardDTO(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return IndividualDebitCardDTO(_id, _type, attributes_to_object(attributes), relationships)


class BusinessDebitCardDTO(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return BusinessDebitCardDTO(_id, _type, attributes_to_object(attributes), relationships)


class BusinessCreditCardDTO(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return BusinessCreditCardDTO(_id, _type, attributes_to_object(attributes), relationships)


class IndividualVirtualDebitCardDTO(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return IndividualVirtualDebitCardDTO(_id, _type, attributes_to_object(attributes), relationships)


class BusinessVirtualDebitCardDTO(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return BusinessVirtualDebitCardDTO(_id, _type, attributes_to_object(attributes), relationships)


class BusinessVirtualCreditCardDTO(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return BusinessVirtualCreditCardDTO(_id, _type, attributes_to_object(attributes), relationships)


Card = Union[IndividualDebitCardDTO, BusinessDebitCardDTO, IndividualVirtualDebitCardDTO, BusinessVirtualDebitCardDTO,
             BusinessVirtualCreditCardDTO, BusinessCreditCardDTO]


class CreateIndividualDebitCard(UnitRequest):
    def __init__(self, relationships: Dict[str, Relationship], shipping_address: Optional[Address] = None,
                 design: Optional[str] = None, idempotency_key: Optional[str] = None,
                 tags: Optional[Dict[str, str]] = None):
        self.shipping_address = shipping_address
        self.design = design
        self.idempotency_key = idempotency_key
        self.tags = tags
        self.relationships = relationships

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "individualDebitCard",
                "attributes": self.vars_to_attributes_dict(),
                "relationships": self.relationships
            }
        }

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())


class CreateBusinessCard(UnitRequest):
    def __init__(self, full_name: FullName, date_of_birth: date, address: Address, phone: Phone, email: str,
                 shipping_address: Optional[Address], ssn: Optional[str] = None, passport: Optional[str] = None,
                 nationality: Optional[str] = None, design: Optional[str] = None, idempotency_key: Optional[str] = None,
                 tags: Optional[Dict[str, str]] = None, relationships: Optional[Dict[str, Relationship]] = None,
                 _type: str = "businessDebitCard"):
        self.full_name = full_name
        self.date_of_birth = date_of_birth
        self.address = address
        self.phone = phone
        self.email = email
        self.shipping_address = shipping_address
        self.ssn = ssn
        self.passport = passport
        self.nationality = nationality
        self.design = design
        self.idempotency_key = idempotency_key
        self.tags = tags
        self.relationships = relationships
        self._type = _type

    def to_json_api(self) -> Dict:
        return self.to_payload(ignore=["_type"])

    def __repr__(self):
        json.dumps(self.to_json_api())


class CreateBusinessDebitCard(CreateBusinessCard):
    def __init__(self, full_name: FullName, date_of_birth: date, address: Address, phone: Phone, email: str,
                 shipping_address: Optional[Address], ssn: Optional[str] = None, passport: Optional[str] = None,
                 nationality: Optional[str] = None, design: Optional[str] = None, idempotency_key: Optional[str] = None,
                 tags: Optional[Dict[str, str]] = None, relationships: Optional[Dict[str, Relationship]] = None):
        CreateBusinessCard.__init__(**locals())


class CreateBusinessCreditCard(CreateBusinessCard):
    def __init__(self, full_name: FullName, date_of_birth: date, address: Address, phone: Phone, email: str,
                 shipping_address: Optional[Address], ssn: Optional[str] = None, passport: Optional[str] = None,
                 nationality: Optional[str] = None, design: Optional[str] = None, idempotency_key: Optional[str] = None,
                 tags: Optional[Dict[str, str]] = None, relationships: Optional[Dict[str, Relationship]] = None):
        CreateBusinessCard.__init__(**locals(), _type="businessCreditCard")


class CreateIndividualVirtualDebitCard(UnitRequest):
    def __init__(self, relationships: Dict[str, Relationship], idempotency_key: Optional[str] = None,
                 tags: Optional[Dict[str, str]] = None):
        self.idempotency_key = idempotency_key
        self.tags = tags
        self.relationships = relationships

    def to_json_api(self) -> Dict:
        return self.to_payload("individualVirtualDebitCard")

    def __repr__(self):
        json.dumps(self.to_json_api())


class CreateBusinessVirtualCard(UnitRequest):
    def __init__(self, full_name: FullName, date_of_birth: date, address: Address, phone: Phone, email: str,
                 ssn: Optional[str] = None, passport: Optional[str] = None, nationality: Optional[str] = None,
                 idempotency_key: Optional[str] = None, tags: Optional[Dict[str, str]] = None,
                 relationships: Optional[Dict[str, Relationship]] = None,
                 _type: str = "businessVirtualDebitCard"):
        self.full_name = full_name
        self.date_of_birth = date_of_birth
        self.address = address
        self.phone = phone
        self.email = email
        self.ssn = ssn
        self.passport = passport
        self.nationality = nationality
        self.idempotency_key = idempotency_key
        self.tags = tags
        self.relationships = relationships
        self._type = _type

    def to_json_api(self) -> Dict:
        return self.to_payload(ignore=["_type"])

    def __repr__(self):
        json.dumps(self.to_json_api())


class CreateBusinessVirtualDebitCard(CreateBusinessVirtualCard):
    def __init__(self, full_name: FullName, date_of_birth: date, address: Address, phone: Phone, email: str,
                 ssn: Optional[str] = None, passport: Optional[str] = None, nationality: Optional[str] = None,
                 idempotency_key: Optional[str] = None, tags: Optional[Dict[str, str]] = None,
                 relationships: Optional[Dict[str, Relationship]] = None):
        CreateBusinessVirtualCard.__init__(**locals())


class CreateBusinessVirtualCreditCard(CreateBusinessVirtualCard):
    def __init__(self, full_name: FullName, date_of_birth: date, address: Address, phone: Phone, email: str,
                 ssn: Optional[str] = None, passport: Optional[str] = None, nationality: Optional[str] = None,
                 idempotency_key: Optional[str] = None, tags: Optional[Dict[str, str]] = None,
                 relationships: Optional[Dict[str, Relationship]] = None):
        CreateBusinessVirtualCard.__init__(**locals(), _type="businessVirtualCreditCard")


CreateCardRequest = Union[CreateIndividualDebitCard, CreateBusinessDebitCard, CreateIndividualVirtualDebitCard,
                          CreateBusinessVirtualDebitCard, CreateBusinessCreditCard, CreateBusinessVirtualCreditCard]


class PatchIndividualDebitCard(UnitRequest):
    def __init__(self, card_id: str, shipping_address: Optional[Address] = None, design: Optional[str] = None,
                 tags: Optional[Dict[str, str]] = None):
        self.card_id = card_id
        self.shipping_address = shipping_address
        self.design = design
        self.tags = tags

    def to_json_api(self) -> Dict:
        return self.to_payload("individualDebitCard")

    def __repr__(self):
        json.dumps(self.to_json_api())


class PatchBusinessCard(UnitRequest):
    def __init__(self, card_id: str, shipping_address: Optional[Address] = None, address: Optional[Address] = None,
                 phone: Optional[Phone] = None, email: Optional[str] = None, design: Optional[str] = None,
                 tags: Optional[Dict[str, str]] = None, _type: str = "businessDebitCard"):
        self.card_id = card_id
        self.shipping_address = shipping_address
        self.address = address
        self.phone = phone
        self.email = email
        self.design = design
        self.tags = tags
        self._type = _type

    def to_json_api(self) -> Dict:
        return self.to_payload(ignore=["card_id", "_type"])

    def __repr__(self):
        json.dumps(self.to_json_api())


class PatchBusinessDebitCard(PatchBusinessCard):
    def __init__(self, card_id: str, shipping_address: Optional[Address] = None, address: Optional[Address] = None,
                 phone: Optional[Phone] = None, email: Optional[str] = None, design: Optional[str] = None,
                 tags: Optional[Dict[str, str]] = None):
        PatchBusinessCard.__init__(**locals())


class PatchBusinessCreditCard(PatchBusinessCard):
    def __init__(self, card_id: str, shipping_address: Optional[Address] = None, address: Optional[Address] = None,
                 phone: Optional[Phone] = None, email: Optional[str] = None, design: Optional[str] = None,
                 tags: Optional[Dict[str, str]] = None):
        PatchBusinessCard.__init__(**locals(), _type="businessCreditCard")


class PatchIndividualVirtualDebitCard(UnitRequest):
    def __init__(self, card_id: str, tags: Optional[Dict[str, str]] = None):
        self.card_id = card_id
        self.tags = tags

    def to_json_api(self) -> Dict:
        return self.to_payload("individualVirtualDebitCard", ignore=["card_id"])

    def __repr__(self):
        json.dumps(self.to_json_api())


class PatchBusinessVirtualCard(UnitRequest):
    def __init__(self, card_id: str, address: Optional[Address] = None, phone: Optional[Phone] = None,
                 email: Optional[str] = None, tags: Optional[Dict[str, str]] = None,
                 _type: str = "businessVirtualDebitCard"):
        self.card_id = card_id
        self.address = address
        self.phone = phone
        self.email = email
        self.tags = tags
        self._type = _type

    def to_json_api(self) -> Dict:
        return self.to_payload(ignore=["card_id", "_type"])


class PatchBusinessVirtualDebitCard(PatchBusinessVirtualCard):
    def __init__(self, card_id: str, address: Optional[Address] = None, phone: Optional[Phone] = None,
                 email: Optional[str] = None, tags: Optional[Dict[str, str]] = None):
        super().__init__(card_id, address, phone, email, tags)


class PatchBusinessVirtualCreditCard(PatchBusinessVirtualCard):
    def __init__(self, card_id: str, address: Optional[Address] = None, phone: Optional[Phone] = None,
                 email: Optional[str] = None, tags: Optional[Dict[str, str]] = None):
        super().__init__(card_id, address, phone, email, tags, "businessVirtualCreditCard")


PatchCardRequest = Union[PatchIndividualDebitCard, PatchBusinessDebitCard, PatchIndividualVirtualDebitCard,
                         PatchBusinessVirtualDebitCard, PatchBusinessCreditCard, PatchBusinessVirtualCreditCard]


class ReplaceCardRequest(object):
    def __init__(self, shipping_address: Optional[Address] = None):
        self.shipping_address = shipping_address

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "replaceCard",
                "attributes": {},
            }
        }

        if self.shipping_address:
            payload["data"]["attributes"]["shippingAddress"] = self.shipping_address

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())


PinStatus = Literal["Set", "NotSet"]


class PinStatusDTO(object):
    def __init__(self, _type: str, attributes: Dict[str, object]):
        self.type = _type
        self.attributes = attributes_to_object(attributes)

    @staticmethod
    def from_json_api(_id, _type, attributes, _relationships):
        return PinStatusDTO(_type, attributes)


class CardLimitsDTO(object):
    def __init__(self, limits: CardLevelLimits, daily_totals: CardTotals, monthly_totals: CardTotals):
        self.type = "limits"
        self.attributes = {"limits": limits, "dailyTotals": daily_totals, "monthlyTotals": monthly_totals}

    @staticmethod
    def from_json_api(attributes):
        limits = CardLevelLimits.from_json_api(attributes.get("limits")) if attributes.get("limits") else None
        return CardLimitsDTO(limits, CardTotals.from_json_api(attributes.get("dailyTotals")),
                             CardTotals.from_json_api(attributes.get("monthlyTotals")))


class ListCardParams(UnitParams):
    def __init__(self, offset: int = 0, limit: int = 100, account_id: Optional[str] = None,
                 customer_id: Optional[str] = None, tags: Optional[object] = None, include: Optional[str] = None,
                 sort: Optional[Literal["createdAt", "-createdAt"]] = None,
                 status: Optional[List[CardStatus]] = None):
        self.offset = offset
        self.limit = limit
        self.account_id = account_id
        self.customer_id = customer_id
        self.tags = tags
        self.include = include
        self.sort = sort
        self.status = status

    def to_dict(self) -> Dict:
        parameters = {"page[limit]": self.limit, "page[offset]": self.offset}
        if self.customer_id:
            parameters["filter[customerId]"] = self.customer_id
        if self.account_id:
            parameters["filter[accountId]"] = self.account_id
        if self.tags:
            parameters["filter[tags]"] = self.tags
        if self.include:
            parameters["include"] = self.include
        if self.sort:
            parameters["sort"] = self.sort
        if self.status:
            for idx, status_filter in enumerate(self.status):
                parameters[f"filter[status][{idx}]"] = status_filter
        return parameters

