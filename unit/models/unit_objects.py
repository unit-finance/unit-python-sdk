from typing import Generic, List, Union, TypeVar
import requests
from unit.models.codecs import DtoDecoder

T = TypeVar('T')


class UnitResponse(Generic[T]):
    def __init__(self, data: Union[T, List[T]], included=None, meta=None):
        self.data = DtoDecoder.decode(data)
        self.included = DtoDecoder.decode(included)
        self.meta = DtoDecoder.decode(meta)

    @staticmethod
    def from_json_api(r: requests.Response, as_text: bool = False):
        if as_text:
            return UnitResponse(r.text)

        if len(r.text) <= 2:
            return UnitResponse([])

        data = r.json().get("data")
        included = r.json().get("included")
        meta = r.json().get("meta")

        return UnitResponse(data, included, meta)
