from typing import Optional, Dict

from unit.models import UnitDTO, UnitParams, Relationship


class TaxFormDTO(UnitDTO):
    def __init__(self, _id: str, _type: str, form_type: str, tax_year: str, relationships: Dict[str, Relationship]):
        self.id = _id
        self.type = _type
        self.attributes = {"formType": form_type, "taxYear": tax_year}
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return TaxFormDTO(_id, _type, attributes["formType"], attributes["taxYear"], relationships)


class ListTaxFormParams(UnitParams):
    def __init__(self, offset: int = 0, limit: int = 100, account_id: Optional[str] = None,
                 customer_id: Optional[str] = None, tax_years: Optional[str] = None,
                 tax_form_types: Optional[str] = None):
        self.offset = offset
        self.limit = limit
        self.account_id = account_id
        self.customer_id = customer_id
        self.tax_years = tax_years
        self.tax_form_types = tax_form_types

    def to_dict(self) -> Dict:
        parameters = {"page[limit]": self.limit, "page[offset]": self.offset}
        if self.customer_id:
            parameters["filter[customerId]"] = self.customer_id
        if self.account_id:
            parameters["filter[accountId]"] = self.account_id
        if self.tax_years:
            parameters["filter[taxYears]"] = self.tax_years
        if self.tax_form_types:
            parameters["filter[taxFormTypes]"] = self.tax_form_types
        return parameters
