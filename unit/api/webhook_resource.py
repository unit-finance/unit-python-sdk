from unit.api.base_resource import BaseResource
from unit.models.webhook import *
from unit.models.codecs import DtoDecoder
import hmac
from hashlib import sha1
import base64


class WebhookResource(BaseResource):
    def __init__(self, api_url, token, retries):
        super().__init__(api_url, token, retries)
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

    def list(self, params: ListWebhookParams = None) -> Union[UnitResponse[List[WebhookDTO]], UnitError]:
        params = params or ListWebhookParams()
        response = super().get(self.resource, params.to_dict())
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

    def verify(self, signature: str, secret: str, payload):
        mac = hmac.new(
            secret.encode(),
            msg=json.dumps(payload, separators=(',', ':'), ensure_ascii=False).encode('utf-8'),
            digestmod=sha1,
        )
        res = base64.encodebytes(mac.digest()).decode().rstrip('\n')
        return res == signature
