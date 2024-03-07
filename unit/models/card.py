from unit.utils import date_utils
from unit.models import *

CardStatus = Literal["Inactive", "Active", "Stolen", "Lost", "Frozen", "ClosedByCustomer", "SuspectedFraud"]


class IndividualDebitCardDTO(object):
    def __init__(self, id: str, created_at: datetime, last_4_digits: str, expiration_date: str, status: CardStatus,
                 shipping_address: Optional[Address], design: Optional[str],
                 relationships: Optional[Dict[str, Relationship]], tags: Optional[Dict[str, str]]):
        self.id = id
        self.type = "individualDebitCard"
        self.attributes = {"createdAt": created_at, "last4Digits": last_4_digits, "expirationDate": expiration_date,
                           "status": status, "shippingAddress": shipping_address, "design": design, "tags": tags}
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        shipping_address = Address.from_json_api(attributes.get("shippingAddress")) if attributes.get("shippingAddress") else None
        return IndividualDebitCardDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), attributes["last4Digits"],
            attributes["expirationDate"], attributes["status"],
            shipping_address, attributes.get("design"), relationships, attributes.get("tags"))


class BusinessCardDTO(object):
    def __init__(self, _id: str, _type: str, created_at: datetime, last_4_digits: str, expiration_date: str,
                 ssn: Optional[str], full_name: FullName, date_of_birth: date, address: Address, phone: Phone,
                 email: str, status: CardStatus, passport: Optional[str], nationality: Optional[str],
                 shipping_address: Optional[Address], design: Optional[str],
                 relationships: Optional[Dict[str, Relationship]], tags: Optional[Dict[str, str]]):
        self.id = _id
        self.type = _type
        self.attributes = {"createdAt": created_at, "last4Digits": last_4_digits, "expirationDate": expiration_date,
                           "ssn": ssn, "fullName": full_name, "dateOfBirth": date_of_birth, "address": address,
                           "phone": phone, "email": email, "status": status, "passport": passport,
                           "nationality": nationality, "shippingAddress": shipping_address, "design": design,
                           "tags": tags}
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return BusinessCardDTO(
            _id, _type, date_utils.to_datetime(attributes["createdAt"]), attributes["last4Digits"],
            attributes["expirationDate"], attributes.get("ssn"), FullName.from_json_api(attributes["fullName"]),
            attributes["dateOfBirth"], Address.from_json_api(attributes["address"]),
            Phone.from_json_api(attributes["phone"]), attributes["email"], attributes["status"],
            attributes.get("passport"), attributes.get("nationality"),
            Address.from_json_api(attributes.get("shippingAddress")), attributes.get("design"), relationships,
            attributes.get("tags")
        )


class BusinessDebitCardDTO(BusinessCardDTO):
    def __init__(self, card: BusinessCardDTO):
        self.id = card.id
        self.type = card.type
        self.attributes = card.attributes
        self.relationships = card.relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return BusinessDebitCardDTO(BusinessCardDTO.from_json_api(_id, _type, attributes, relationships))


class BusinessCreditCardDTO(BusinessCardDTO):
    def __init__(self, card: BusinessCardDTO):
        self.id = card.id
        self.type = card.type
        self.attributes = card.attributes
        self.relationships = card.relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return BusinessCreditCardDTO(BusinessCardDTO.from_json_api(_id, _type, attributes, relationships))


class IndividualVirtualDebitCardDTO(object):
    def __init__(self, _id: str, created_at: datetime, last_4_digits: str, expiration_date: str, status: CardStatus,
                 relationships: Optional[Dict[str, Relationship]], tags: Optional[Dict[str, str]]):
        self.id = _id
        self.type = "individualVirtualDebitCard"
        self.attributes = {"createdAt": created_at, "last4Digits": last_4_digits, "expirationDate": expiration_date,
                           "status": status, "tags": tags}
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return IndividualVirtualDebitCardDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), attributes["last4Digits"],
            attributes["expirationDate"], attributes["status"], relationships, attributes.get("tags")
        )


class BusinessVirtualCardDTO(object):
    def __init__(self, _id: str, _type: str, created_at: datetime, last_4_digits: str, expiration_date: str,
                 ssn: Optional[str], full_name: FullName, date_of_birth: date, address: Address, phone: Phone,
                 email: str, status: CardStatus, passport: Optional[str], nationality: Optional[str],
                 relationships: Optional[Dict[str, Relationship]], tags: Optional[Dict[str, str]]):
        self.id = _id
        self.type = _type
        self.attributes = {"createdAt": created_at, "last4Digits": last_4_digits, "expirationDate": expiration_date,
                           "ssn": ssn, "fullName": full_name, "dateOfBirth": date_of_birth, "address": address,
                           "phone": phone, "email": email, "status": status, "passport": passport,
                           "nationality": nationality, "tags": tags}
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return BusinessVirtualCardDTO(
            _id, _type, date_utils.to_datetime(attributes["createdAt"]), attributes["last4Digits"],
            attributes["expirationDate"], attributes.get("ssn"), FullName.from_json_api(attributes["fullName"]),
            attributes["dateOfBirth"], Address.from_json_api(attributes["address"]),
            Phone.from_json_api(attributes["phone"]), attributes["email"], attributes["status"],
            attributes.get("passport"), attributes.get("nationality"), relationships, attributes.get("tags"))


class BusinessVirtualDebitCardDTO(BusinessVirtualCardDTO):
    def __init__(self, card: BusinessVirtualCardDTO):
        self.id = card.id
        self.type = card.type
        self.attributes = card.attributes
        self.relationships = card.relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return BusinessVirtualDebitCardDTO(BusinessVirtualCardDTO.from_json_api(_id, _type, attributes, relationships))


class BusinessVirtualCreditCardDTO(BusinessVirtualCardDTO):
    def __init__(self, card: BusinessVirtualCardDTO):
        self.id = card.id
        self.type = card.type
        self.attributes = card.attributes
        self.relationships = card.relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return BusinessVirtualCreditCardDTO(BusinessVirtualCardDTO.from_json_api(_id, _type, attributes, relationships))


Card = Union[IndividualDebitCardDTO, BusinessDebitCardDTO, IndividualVirtualDebitCardDTO, BusinessVirtualDebitCardDTO,
             BusinessVirtualCreditCardDTO, BusinessCreditCardDTO]


class CreateIndividualDebitCard(UnitRequest):
    def __init__(self, relationships: Dict[str, Relationship], shipping_address: Optional[Address] = None,
                 design: Optional[str] = None, idempotency_key: Optional[str] = None,
                 tags: Optional[Dict[str, str]] = None, limits: Optional[CardLevelLimits] = None,
                 additional_embossed_text: Optional[str] = None, print_only_business_name: Optional[str] = None,
                 expiry_date: Optional[str] = None):
        self.shipping_address = shipping_address
        self.design = design
        self.idempotency_key = idempotency_key
        self.tags = tags
        self.limits = limits
        self.expiry_date = expiry_date
        self.additional_embossed_text = additional_embossed_text
        self.print_only_business_name = print_only_business_name
        self.relationships = relationships

    def to_json_api(self) -> Dict:
        return super().to_payload("individualDebitCard")

    def __repr__(self):
        return json.dumps(self.to_json_api())


class CreateBusinessCard(UnitRequest):
    def __init__(self, full_name: FullName, date_of_birth: date, address: Address, phone: Phone, email: str,
                 relationships: Dict[str, Relationship], shipping_address: Optional[Address] = None,
                 ssn: Optional[str] = None, passport: Optional[str] = None, nationality: Optional[str] = None,
                 design: Optional[str] = None, idempotency_key: Optional[str] = None,
                 tags: Optional[Dict[str, str]] = None, limits: Optional[CardLevelLimits] = None,
                 additional_embossed_text: Optional[str] = None, print_only_business_name: Optional[bool] = None,
                 expiry_date: Optional[str] = None):
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
        self.limits = limits
        self.additional_embossed_text = additional_embossed_text
        self.print_only_business_name = print_only_business_name
        self.expiry_date = expiry_date

    def to_json_api(self, _type: str) -> Dict:
        return super().to_payload(_type)

    def __repr__(self):
        return json.dumps(self.to_json_api())


class CreateBusinessDebitCard(CreateBusinessCard):
    def to_json_api(self):
        return super().to_json_api("businessDebitCard")


class CreateBusinessCreditCard(CreateBusinessCard):
    def to_json_api(self):
        return super().to_json_api("businessCreditCard")


class CreateIndividualVirtualDebitCard(UnitRequest):
    def __init__(self, relationships: Dict[str, Relationship], idempotency_key: Optional[str] = None,
                 tags: Optional[Dict[str, str]] = None, expiry_date: Optional[str] = None):
        self.idempotency_key = idempotency_key
        self.tags = tags
        self.relationships = relationships
        self.expiry_date = expiry_date

    def to_json_api(self) -> Dict:
        return super().to_payload("individualVirtualDebitCard")

    def __repr__(self):
        return json.dumps(self.to_json_api())


class CreateBusinessVirtualCard(UnitRequest):
    def __init__(self, full_name: FullName, date_of_birth: date, address: Address, phone: Phone, email: str,
                 relationships: Dict[str, Relationship], ssn: Optional[str] = None, passport: Optional[str] = None,
                 nationality: Optional[str] = None, idempotency_key: Optional[str] = None,
                 tags: Optional[Dict[str, str]] = None, limits: Optional[CardLevelLimits] = None,
                 expiry_date: Optional[str] = None):
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
        self.limits = limits
        self.expiry_date = expiry_date

    def to_json_api(self, _type: str) -> Dict:
        return super().to_payload(_type)

    def __repr__(self):
        return json.dumps(self.to_json_api())


class CreateBusinessVirtualDebitCard(CreateBusinessVirtualCard):
    def to_json_api(self):
        return super().to_json_api("businessVirtualDebitCard")


class CreateBusinessVirtualCreditCard(CreateBusinessVirtualCard):
    def to_json_api(self):
        return super().to_json_api("businessVirtualCreditCard")


CreateCardRequest = Union[CreateIndividualDebitCard, CreateBusinessDebitCard, CreateIndividualVirtualDebitCard,
                          CreateBusinessVirtualDebitCard, CreateBusinessVirtualCreditCard, CreateBusinessCreditCard]


class PatchIndividualDebitCard(UnitRequest):
    def __init__(self, card_id: str, shipping_address: Optional[Address] = None, design: Optional[str] = None,
                 tags: Optional[Dict[str, str]] = None, limits: Optional[CardLevelLimits] = None):
        self.card_id = card_id
        self.shipping_address = shipping_address
        self.design = design
        self.tags = tags
        self.limits = limits

    def to_json_api(self) -> Dict:
        return super().to_payload("individualDebitCard", ignore=["card_id"])

    def __repr__(self):
        return json.dumps(self.to_json_api())


class PatchBusinessCard(UnitRequest):
    def __init__(self, card_id: str, shipping_address: Optional[Address] = None, address: Optional[Address] = None,
                 phone: Optional[Phone] = None, email: Optional[str] = None, design: Optional[str] = None,
                 tags: Optional[Dict[str, str]] = None, limits: Optional[CardLevelLimits] = None):
        self.card_id = card_id
        self.shipping_address = shipping_address
        self.address = address
        self.phone = phone
        self.email = email
        self.design = design
        self.tags = tags
        self.limits = limits

    def to_json_api(self, _type: str = "businessDebitCard") -> Dict:
        return super().to_payload(_type, ignore=["card_id"])

    def __repr__(self):
        return json.dumps(self.to_json_api())


class PatchBusinessDebitCard(PatchBusinessCard):
    pass


class PatchBusinessCreditCard(PatchBusinessCard):
    def to_json_api(self) -> Dict:
        return super().to_json_api("businessCreditCard")


class PatchIndividualVirtualDebitCard(UnitRequest):
    def __init__(self, card_id: str, tags: Optional[Dict[str, str]] = None, limits: Optional[CardLevelLimits] = None):
        self.card_id = card_id
        self.tags = tags
        self.limits = limits

    def to_json_api(self) -> Dict:
        return super().to_payload("individualVirtualDebitCard", ignore=["card_id"])

    def __repr__(self):
        return json.dumps(self.to_json_api())


class PatchBusinessVirtualCard(UnitRequest):
    def __init__(self, card_id: str, address: Optional[Address] = None, phone: Optional[Phone] = None,
                 email: Optional[str] = None, tags: Optional[Dict[str, str]] = None,
                 _type: str = "businessVirtualDebitCard", limits: Optional[CardLevelLimits] = None):
        self.card_id = card_id
        self.address = address
        self.phone = phone
        self.email = email
        self.tags = tags
        self.limits = limits

    def to_json_api(self, _type: str = "businessVirtualDebitCard") -> Dict:
        return super().to_payload(_type, igonre=["card_id"])


class PatchBusinessVirtualDebitCard(PatchBusinessVirtualCard):
    pass


class PatchBusinessVirtualCreditCard(PatchBusinessVirtualCard):
    def to_json_api(self) -> Dict:
        return super().to_json_api("businessVirtualCreditCard")


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
        return json.dumps(self.to_json_api())


PinStatus = Literal["Set", "NotSet"]


class PinStatusDTO(object):
    def __init__(self, status: PinStatus):
        self.type = "pinStatus"
        self.attributes = {"status": status}

    @staticmethod
    def from_json_api(attributes):
        return PinStatusDTO(attributes["status"])


class CardLimitsDTO(object):
    def __init__(self, limits: Optional[CardLevelLimits] = None, daily_totals: [CardTotals] = None,
                 monthly_totals: Optional[CardTotals] = None):
        self.type = "limits"
        self.attributes = {"limits": limits, "dailyTotals": daily_totals, "monthlyTotals": monthly_totals}

    @staticmethod
    def from_json_api(attributes):
        return CardLimitsDTO(CardLevelLimits.from_json_api(attributes.get("limits")),
                             CardTotals.from_json_api(attributes.get("dailyTotals")),
                             CardTotals.from_json_api(attributes.get("monthlyTotals")))


class ListCardParams(UnitParams):
    def __init__(self, offset: int = 0, limit: int = 100, account_id: Optional[str] = None,
                 customer_id: Optional[str] = None, tags: Optional[Dict[str, str]] = None, include: Optional[str] = None,
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
            parameters["filter[tags]"] = json.dumps(self.tags)
        if self.include:
            parameters["include"] = self.include
        if self.sort:
            parameters["sort"] = self.sort
        if self.status:
            for idx, status_filter in enumerate(self.status):
                parameters[f"filter[status][{idx}]"] = status_filter
        return parameters


class GetMobileWalletPayloadRequest(UnitRequest):
    def __init__(self, card_id: str, signed_nonce: str, secure_path: Optional[str] = "https://secure.api.s.unit.sh"):
        self.card_id = card_id
        self.signed_nonce = signed_nonce
        self.secure_path = secure_path

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "attributes": {
                    "signedNonce": self.signed_nonce
                }
            }
        }
        return payload

    def __repr__(self):
        return json.dumps(self.to_json_api())


class MobileWalletPayloadDTO(object):
    def __init__(self, payload: str):
        self.type = "mobileWalletPayload"
        self.attributes = {"payload": payload}

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return MobileWalletPayloadDTO(attributes["payload"])


class EnableCardToCardPaymentsRequest(UnitRequest):
    def __init__(self, card_id: str, astra_token: str, idempotency_key: Optional[str] = None):
        self.card_id = card_id
        self.astra_token = astra_token
        self.idempotency_key = idempotency_key

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "astra",
                "attributes": {
                    "token": self.astra_token
                }
            }
        }

        if self.idempotency_key:
            payload["data"]["attributes"]["idempotencyKey"] = self.idempotency_key

        return payload

    def __repr__(self):
        return json.dumps(self.to_json_api())


class CardToCardPaymentDTO(object):
    def __init__(self, _type: str, _id: str, astra_card_id: str):
        self._type = _type
        self._id = _id
        self.astra_card_id = astra_card_id

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CardToCardPaymentDTO(_id, _type, attributes["astraCardId"])
