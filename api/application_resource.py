from api.base_resource import BaseResource
from models.application import *
from models.codecs import DtoDecoder


class ApplicationResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "applications"

    def create(self, request: Union[CreateIndividualApplicationRequest, CreateBusinessApplicationRequest]) -> Union[UnitResponse[ApplicationDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post(self.resource, payload)

        if response.ok:
            data = response.json().get("data")
            included = response.json().get("included")
            # alex todo: implement document and then decode & pass the included section instead of None to UnitResponse
            if data["type"] == "individualApplication":
                return UnitResponse[IndividualApplicationDTO](DtoDecoder.decode(data), None)
            else:
                return UnitResponse[BusinessApplicationDTO](DtoDecoder.decode(data), None)

        else:
            return UnitError.from_json_api(response.json())

    def list(self, offset: int = 0, limit: int = 100) -> Union[UnitResponse[list[ApplicationDTO]], UnitError]:
        response = super().get(self.resource, {"page[limit]": limit, "page[offset]": offset})
        if response.status_code == 200:
            data = response.json().get("data")
            included = response.json().get("included")
            # alex todo: implement document and then decode & pass the included section instead of None to UnitResponse

            return UnitResponse[ApplicationDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())


    def list_documents(self, applicationId: str):
        response = super().get(f"{self.resource}/{applicationId}/documents")
        if response.status_code == 200:
            data = response.json().get("data")
            return UnitResponse[ApplicationDocumentDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    # def get(self, applicationId: str)-> Union[UnitResponse[ApplicationDTO], UnitError]:
    #     response = super().get(f"{self.resource}/{applicationId}")
    #     if response.status_code == 200:
    #         data = response.json().get("data")
    #         included = response.json().get("included")
    #
    #         return UnitResponse[ApplicationDTO](DtoDecoder.decode(data), None)
    #     else:
    #         return UnitError.from_json_api(response.json())

