from unit.api.base_resource import BaseResource
from unit.models.webhook import *
from unit.models.codecs import DtoDecoder


class WebhookResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "webhooks"

    def create(self, request: CreateWebhookRequest) -> Union[UnitResponse[WebhookDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post(self.resource, payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[WebhookDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def get(self, webhook_id: str) -> Union[UnitResponse[WebhookDTO], UnitError]:
        response = super().get(f"{self.resource}/{webhook_id}")
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[WebhookDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def list(self, offset: int = 0, limit: int = 100) -> Union[UnitResponse[list[WebhookDTO]], UnitError]:
        response = super().get(self.resource, {"page[limit]": limit, "page[offset]": offset})
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[WebhookDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def update(self, request: PatchWebhookRequest) -> Union[UnitResponse[WebhookDTO], UnitError]:
        payload = request.to_json_api()
        response = super().patch(f"{self.resource}/{request.webhook_id}", payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[WebhookDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def enable(self, webhook_id: str) -> Union[UnitResponse[WebhookDTO], UnitError]:
        response = super().post(f"{self.resource}/{webhook_id}/enable")
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[WebhookDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def disable(self, webhook_id: str) -> Union[UnitResponse[WebhookDTO], UnitError]:
        response = super().post(f"{self.resource}/{webhook_id}/disable")
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[WebhookDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

