from unit.api.base_resource import BaseResource
from unit.models.webhook import *
import hmac
from hashlib import sha1
import base64
from unit.models.unit_objects import UnitResponse

ReturnType = Union[UnitResponse[WebhookDTO], UnitError]


class WebhookResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token, return_type=WebhookDTO)
        self.resource = "webhooks"

    def create(self, request: CreateWebhookRequest) -> ReturnType:
        payload = request.to_json_api()
        return super().post(self.resource, payload)

    def get(self, webhook_id: str) -> ReturnType:
        return super().get(f"{self.resource}/{webhook_id}")

    def list(self, params: ListWebhookParams = None) -> Union[UnitResponse[List[WebhookDTO]], UnitError]:
        params = params or ListWebhookParams()
        return super().get(self.resource, params.to_dict(), return_type=List[WebhookDTO])

    def update(self, request: PatchWebhookRequest) -> ReturnType:
        payload = request.to_json_api()
        return super().patch(f"{self.resource}/{request.webhook_id}", payload)

    def enable(self, webhook_id: str) -> ReturnType:
        return super().post(f"{self.resource}/{webhook_id}/enable")

    def disable(self, webhook_id: str) -> ReturnType:
        return super().post(f"{self.resource}/{webhook_id}/disable")

    def verify(self, signature: str, secret: str, payload):
        mac = hmac.new(
            secret.encode(),
            msg=json.dumps(payload, separators=(',', ':'), ensure_ascii=False).encode('utf-8'),
            digestmod=sha1,
        )
        res = base64.encodebytes(mac.digest()).decode().rstrip('\n')
        return res == signature
