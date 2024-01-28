from unit.utils.configuration import Configuration
from unit.api.base_resource import BaseResource
from unit.models.statement import *
from unit.models.codecs import DtoDecoder


class TaxFormResource(BaseResource):
    def __init__(self, configuration: Configuration):
        super().__init__("tax-forms", configuration)

    def get(self, tax_form_id: str) -> Union[UnitResponse[TaxFormDTO], UnitError]:
        response = super().get(f"{self.resource}/{tax_form_id}")

        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[TaxFormDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def get_pdf(self, tax_form_id: str) -> Union[UnitResponse[TaxFormDTO], UnitError]:
        response = super().get(f"{self.resource}/{tax_form_id}/pdf")

        if super().is_20x(response.status_code):
            return UnitResponse[bytes](response.content, None)
        else:
            return UnitError.from_json_api(response.json())

    def list(self) -> Union[UnitResponse[List[TaxFormDTO]], UnitError]:
        response = super().get(self.resource)

        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[TaxFormDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

