from unit.models import *

ApplicationFormStage = Literal["ChooseBusinessOrIndividual", "EnterIndividualInformation",
                               "IndividualApplicationCreated", "EnterBusinessInformation", "EnterOfficerInformation",
                               "EnterBeneficialOwnersInformation", "BusinessApplicationCreated",
                               "EnterSoleProprietorshipInformation", "SoleProprietorshipApplicationCreated"]


class ApplicationFormPrefill(UnitDTO):
    def __init__(self, application_type: Optional[str], full_name: Optional[FullName], ssn: Optional[str],
                 passport: Optional[str], nationality: Optional[str], date_of_birth: Optional[date],
                 email: Optional[str], name: Optional[str], state_of_incorporation: Optional[str],
                 entity_type: Optional[str], contact: Optional[BusinessContact], officer: Optional[Officer],
                 beneficial_owners: [BeneficialOwner], website: Optional[str], dba: Optional[str],
                 ein: Optional[str], address: Optional[Address], phone: Optional[Phone]):
        self.application_type = application_type
        self.full_name = full_name
        self.ssn = ssn
        self.passport = passport
        self.nationality = nationality
        self.date_of_birth = date_of_birth
        self.email = email
        self.name = name
        self.state_of_incorporation = state_of_incorporation
        self.entity_type = entity_type
        self.contact = contact
        self.officer = officer
        self.beneficial_owners = beneficial_owners
        self.website = website
        self.dba = dba
        self.ein = ein
        self.address = address
        self.phone = phone


class ApplicationFormDTO(UnitDTO):
    def __init__(self, id: str, url: str, stage: ApplicationFormStage, applicant_details: ApplicationFormPrefill,
                 tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        self.id = id
        self.type = "applicationForm"
        self.attributes = {"url": url, "stage": stage, "applicantDetails": applicant_details, "tags": tags}
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return ApplicationFormDTO(_id, attributes["url"], attributes["stage"], attributes.get("applicantDetails"),
                                  attributes.get("tags"), relationships)


AllowedApplicationTypes = Union["Individual", "Business", "SoleProprietorship"]


class ApplicationFormSettingsOverride(UnitDTO):
    def __init__(self, redirect_url: str, privacy_policy_url: str, electronic_disclosures_url: str,
                 deposit_terms_url: str, client_terms_url: str, cardholder_terms_url: str, cash_advanced_terms_url: str,
                 debit_card_disclosure_url: str, additional_disclosures: [Dict[str, str]]):
        self.redirect_url = redirect_url
        self.privacy_policy_url = privacy_policy_url
        self.electronic_disclosures_url = electronic_disclosures_url
        self.deposit_terms_url = deposit_terms_url
        self.client_terms_url = client_terms_url
        self.cardholder_terms_url = cardholder_terms_url
        self.cash_advanced_terms_url = cash_advanced_terms_url
        self.debit_card_disclosure_url = debit_card_disclosure_url
        self.additional_disclosures = additional_disclosures


class CreateApplicationFormRequest(UnitRequest):
    def __init__(self, tags: Optional[Dict[str, str]] = None,
                 application_details: Optional[ApplicationFormPrefill] = None,
                 allowed_application_types: Optional[List[AllowedApplicationTypes]] = None,
                 settings_override: Optional[ApplicationFormSettingsOverride] = None, lang: Optional[str] = None):
        self.tags = tags
        self.application_details = application_details
        self.allowed_application_types = allowed_application_types
        self.lang = lang
        self.settings_override = settings_override

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "applicationForm",
                "attributes": {}
            }
        }

        if self.tags:
            payload["data"]["attributes"]["tags"] = self.tags

        if self.application_details:
            payload["data"]["attributes"]["applicantDetails"] = self.application_details

        if self.allowed_application_types:
            payload["data"]["attributes"]["allowedApplicationTypes"] = self.allowed_application_types

        if self.settings_override:
            payload["data"]["attributes"]["settingsOverride"] = self.settings_override

        if self.lang:
            payload["data"]["attributes"]["lang"] = self.lang

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())


class ListApplicationFormParams(UnitParams):
    def __init__(self, offset: int = 0, limit: int = 100, tags: Optional[object] = None,
                 sort: Optional[Literal["createdAt", "-createdAt"]] = None):
        self.offset = offset
        self.limit = limit
        self.tags = tags
        self.sort = sort

    def to_dict(self) -> Dict:
        parameters = {"page[limit]": self.limit, "page[offset]": self.offset}
        if self.tags:
            parameters["filter[tags]"] = self.tags
        if self.sort:
            parameters["sort"] = self.sort
        return parameters

