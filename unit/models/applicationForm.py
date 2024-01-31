from unit.models import *

ApplicationFormStage = Literal["ChooseBusinessOrIndividual", "EnterIndividualInformation",
                               "IndividualApplicationCreated", "EnterBusinessInformation", "EnterOfficerInformation",
                               "EnterBeneficialOwnersInformation", "BusinessApplicationCreated",
                               "EnterSoleProprietorshipInformation", "SoleProprietorshipApplicationCreated"]

ApplicationFormType = Literal["Individual", "Business", "SoleProprietorship"]


class ApplicationFormPrefill(UnitDTO):
    def __init__(self, application_type: Optional[ApplicationFormType] = None, full_name: Optional[FullName] = None,
                 ssn: Optional[str] = None, passport: Optional[str] = None, nationality: Optional[str] = None,
                 date_of_birth: Optional[date] = None, email: Optional[str] = None, name: Optional[str] = None,
                 state_of_incorporation: Optional[str] = None, entity_type: Optional[str] = None,
                 contact: Optional[BusinessContact] = None, officer: Optional[Officer] = None,
                 beneficial_owners: [List[BeneficialOwner]] = None, website: Optional[str] = None,
                 dba: Optional[str] = None, ein: Optional[str] = None, address: Optional[Address] = None,
                 phone: Optional[Phone] = None, occupation: Optional[str] = None, annual_income: Optional[str] = None,
                 source_of_income: Optional[str] = None, business_vertical: Optional[str] = None,
                 annual_revenue: Optional[str] = None, number_of_employees: Optional[str] = None,
                 cash_flow: Optional[str] = None, year_of_incorporation: Optional[str] = None,
                 countries_of_operation: Optional[List[str]] = None, stock_symbol: Optional[str] = None,
                 has_non_us_entities: Optional[str] = None):
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
        self.occupation = occupation
        self.annual_income = annual_income
        self.source_of_income = source_of_income
        self.business_vertical = business_vertical
        self.annual_revenue = annual_revenue
        self.number_of_employees = number_of_employees
        self.cash_flow = cash_flow
        self.year_of_incorporation = year_of_incorporation
        self.countries_of_operation = countries_of_operation
        self.stock_symbol = stock_symbol
        self.has_non_us_entities = has_non_us_entities


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


class RequireIdVerification(UnitDTO):
    def __init__(self, individual: Optional[bool] = None, officer: Optional[bool] = None,
                 beneficial_owners: Optional[bool] = None):
        self.individual = individual
        self.officer = officer
        self.beneficial_owners = beneficial_owners


class CreateApplicationFormRequest(UnitRequest):
    def __init__(self, tags: Optional[Dict[str, str]] = None,
                 applicant_details: Optional[ApplicationFormPrefill] = None,
                 allowed_application_types: Optional[List[AllowedApplicationTypes]] = None,
                 settings_override: Optional[ApplicationFormSettingsOverride] = None, lang: Optional[str] = None,
                 relationships: Optional[Dict[str, Dict[str, Relationship]]] = None,
                 require_id_verification: Optional[RequireIdVerification] = None,
                 hide_application_progress_tracker: Optional[bool] = None):
        self.tags = tags
        self.applicant_details = applicant_details
        self.allowed_application_types = allowed_application_types
        self.lang = lang
        self.settings_override = settings_override
        self.relationships = relationships
        self.require_id_verification = require_id_verification
        self.hide_application_progress_tracker = hide_application_progress_tracker

    def to_json_api(self) -> Dict:
        return super().to_payload("applicationForm", self.relationships)

    def __repr__(self):
        return json.dumps(self.to_json_api())


class ListApplicationFormParams(UnitParams):
    def __init__(self, offset: int = 0, limit: int = 100, tags: Optional[Dict[str, str]] = None,
                 sort: Optional[Literal["createdAt", "-createdAt"]] = None):
        self.offset = offset
        self.limit = limit
        self.tags = tags
        self.sort = sort

    def to_dict(self) -> Dict:
        parameters = {"page[limit]": self.limit, "page[offset]": self.offset}
        if self.tags:
            parameters["filter[tags]"] = json.dumps(self.tags)
        if self.sort:
            parameters["sort"] = self.sort
        return parameters

