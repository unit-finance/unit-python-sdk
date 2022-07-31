import json
from typing import Optional, Dict
import requests
from unit.models import UnitError, RawUnitObject
from unit.models.unit_objects import UnitResponse
from unit.models.codecs import UnitEncoder


class BaseResource(object):
    def __init__(self, api_url, token, return_type=RawUnitObject):
        self.api_url = api_url.rstrip("/")
        self.token = token
        self.headers = {
            "content-type": "application/vnd.api+json",
            "authorization": f"Bearer {self.token}",
            "user-agent": "unit-python-sdk"
        }
        self.return_type = return_type

    def get(self, resource: str, params: Dict = None, headers: Optional[Dict[str, str]] = None,
            return_type=None, as_text=False):
        response = requests.get(f"{self.api_url}/{resource}", params=params, headers=self.__merge_headers(headers))
        return_type = self.return_type if return_type is None else return_type
        if self.is_20x(response.status_code):
            return UnitResponse[return_type].from_json_api(response, as_text)
        else:
            return UnitError.from_json_api(response.json())

    def post(self, resource: str, data: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None,
             return_type=None):
        data = json.dumps(data, cls=UnitEncoder) if data is not None else None
        return_type = self.return_type if return_type is None else return_type
        response = requests.post(f"{self.api_url}/{resource}", data=data, headers=self.__merge_headers(headers))
        if self.is_20x(response.status_code):
            return UnitResponse[return_type].from_json_api(response)
        else:
            return UnitError.from_json_api(response.json())

    def patch(self, resource: str, data: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None,
              return_type=None):
        data = json.dumps(data, cls=UnitEncoder) if data is not None else None
        response = requests.patch(f"{self.api_url}/{resource}", data=data, headers=self.__merge_headers(headers))
        return_type = self.return_type if return_type is None else return_type
        if self.is_20x(response.status_code):
            return UnitResponse[return_type].from_json_api(response)
        else:
            return UnitError.from_json_api(response.json())

    def delete(self, resource: str, params: Dict = None, headers: Optional[Dict[str, str]] = None,
               return_type=None):
        response = requests.delete(f"{self.api_url}/{resource}", params=params, headers=self.__merge_headers(headers))
        return_type = self.return_type if return_type is None else return_type
        if self.is_20x(response.status_code):
            return UnitResponse[return_type].from_json_api(response)
        else:
            return UnitError.from_json_api(response.json())

    def put(self, resource: str, data: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None,
            return_type=None):
        response = requests.put(f"{self.api_url}/{resource}", data=data, headers=self.__merge_headers(headers))
        return_type = self.return_type if return_type is None else return_type
        if self.is_20x(response.status_code):
            return UnitResponse[return_type].from_json_api(response)
        else:
            return UnitError.from_json_api(response.json())

    def __merge_headers(self, headers: Optional[Dict[str, str]] = None):
        if not headers:
            return self.headers
        else:
            merged = self.headers.copy()
            merged.update(**headers)
            return merged

    def is_20x(self, status: int):
        return status == 200 or status == 201 or status == 204

