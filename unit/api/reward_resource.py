from typing import Union, List, Optional
from unit.api.base_resource import BaseResource
from unit.models import UnitError
from unit.models.reward import RewardDTO, ListRewardsParams, CreateRewardRequest
from unit.models.unit_objects import UnitResponse

ReturnType = Union[UnitResponse[RewardDTO], UnitError]


class RewardResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token, return_type=RewardDTO)
        self.resource = "rewards"

    def create(self, request: CreateRewardRequest) -> ReturnType:
        payload = request.to_json_api()
        return super().post(self.resource, payload)

    def get(self, reward_id: str, include: Optional[str] = "") -> ReturnType:
        return super().get(f"{self.resource}/{reward_id}", {"include": include})

    def list(self, params: ListRewardsParams = None) -> Union[UnitResponse[List[RewardDTO]], UnitError]:
        params = params or ListRewardsParams()
        return super().get(self.resource, params.to_dict(), return_type=List[RewardDTO])
