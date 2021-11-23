from unit.api.base_resource import BaseResource
from unit.models.statement import *
from unit.models.codecs import DtoDecoder


class StatementResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "statements"

    def get_html(self, statement_id: str, language: Optional[str] = "en") -> Union[UnitResponse[str], UnitError]:
        response = super().get(f"{self.resource}/{statement_id}/html", {"language": language})
        if response.status_code == 200:
            return UnitResponse[str](response.text, None)
        else:
            return UnitError.from_json_api(response.json())

    def get_pdf(self, statement_id: str, language: Optional[str] = "en") -> Union[UnitResponse[str], UnitError]:
        response = super().get(f"{self.resource}/{statement_id}/pdf", {"language": language})
        if response.status_code == 200:
            return UnitResponse[str](response.text, None)
        else:
            return UnitError.from_json_api(response.json())

    def list(self, offset: int = 0, limit: int = 100) -> Union[UnitResponse[list[StatementDTO]], UnitError]:
        response = super().get(self.resource, {"page[limit]": limit, "page[offset]": offset})
        if response.status_code == 200:
            data = response.json().get("data")
            return UnitResponse[StatementDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

