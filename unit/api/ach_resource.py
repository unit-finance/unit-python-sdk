from unit.api.base_resource import BaseResource
from unit.models.payment import *
from unit.models.codecs import DtoDecoder, split_json_api_single_response


class AchResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "ach"

    def simulate_transmit(self, request: SimulateTransmitAchRequest) -> Union[UnitResponse[PaymentDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post(f"sandbox/{self.resource}/transmit", payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            # TODO Fix dto
            _id, _type, attributes, relationships = split_json_api_single_response(data)
            print("simulate_transmit")
            print("data", data)
            print("_id, _type, attributes, relationships", _id, _type, attributes, relationships)
            return UnitResponse[SimulateAchPaymentDTO](SimulateAchPaymentDTO.from_json_api(_id, _type, attributes, relationships), None)
        else:
            return UnitError.from_json_api(response.json())

    def simulate_clear(self, request: SimulateClearAchRequest) -> Union[UnitResponse[PaymentDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post(f"sandbox/{self.resource}/clear", payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            # TODO Fix dto
            _id, _type, attributes, relationships = split_json_api_single_response(data)
            return UnitResponse[SimulateAchPaymentDTO](SimulateAchPaymentDTO.from_json_api(_id, _type, attributes, relationships), None)
        else:
            return UnitError.from_json_api(response.json())
