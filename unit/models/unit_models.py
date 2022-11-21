from typing import TypeVar, Generic, Union, List, Dict
from unit.models.codecs import DtoDecoder

T = TypeVar('T')


class UnitResponse(Generic[T]):
    def __init__(self, data: Union[T, List[T]], included=None, meta=None):
        self.data = data
        self.included = included
        self.meta = meta

    @staticmethod
    def from_json_api(json_response, as_text: bool = False):
        if as_text:
            return UnitResponse(json_response.text)

        if not type(json_response) is dict:
            return UnitResponse([])

        data = DtoDecoder.decode(json_response.get("data"))
        included = DtoDecoder.decode(json_response.get("included"))
        meta = DtoDecoder.decode(json_response.get("meta"))

        return UnitResponse(data, included, meta)
