import json
import requests
import backoff

from typing import Optional, Dict
from unit.models.codecs import UnitEncoder

retries = 3
max_time = 300


def fatal_code(e):
    code = e.response.status_code
    print(code)
    return not 500 <= code < 600 or code == 408 or code == 429


class BaseResource(object):
    def __init__(self, api_url, token, retries_amount=3):
        global retries

        self.api_url = api_url.rstrip("/")
        self.token = token
        self.headers = {
            "content-type": "application/vnd.api+json",
            "authorization": f"Bearer {self.token}",
            "user-agent": "unit-python-sdk"
        }
        retries = retries_amount

    @backoff.on_exception(backoff.expo,
                          requests.exceptions.RequestException)
                          # max_tries=retries)
                          # max_time=300,
                          # giveup=fatal_code,
                          # jitter=backoff.random_jitter)
    def get(self, resource: str, params: Dict = None, headers: Optional[Dict[str, str]] = None):
        print("try")
        # try:
        ans = requests.get(f"{self.api_url}/{resource}", params=params, headers=self.__merge_headers(headers))
        # ans.raise_for_status()
        # except requests.exceptions.RequestException as e:
        #     print("except")
        #     print(e)
        #
        # print('good to go')
        return ans

    @backoff.on_exception(backoff.expo,
                          requests.exceptions.RequestException,
                          max_tries=retries,
                          max_time=300,
                          giveup=fatal_code,
                          jitter=backoff.random_jitter)
    def post(self, resource: str, data: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None):
        data = json.dumps(data, cls=UnitEncoder) if data is not None else None
        return requests.post(f"{self.api_url}/{resource}", data=data, headers=self.__merge_headers(headers))

    @backoff.on_exception(backoff.expo,
                          requests.exceptions.RequestException,
                          max_tries=retries,
                          max_time=300,
                          giveup=fatal_code,
                          jitter=backoff.random_jitter)
    def patch(self, resource: str, data: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None):
        data = json.dumps(data, cls=UnitEncoder) if data is not None else None
        return requests.patch(f"{self.api_url}/{resource}", data=data, headers=self.__merge_headers(headers))

    @backoff.on_exception(backoff.expo,
                          requests.exceptions.RequestException,
                          max_tries=retries,
                          max_time=300,
                          giveup=fatal_code,
                          jitter=backoff.random_jitter)
    def delete(self, resource: str, params: Dict = None, headers: Optional[Dict[str, str]] = None):
        return requests.delete(f"{self.api_url}/{resource}", params=params, headers=self.__merge_headers(headers))

    @backoff.on_exception(backoff.expo,
                          requests.exceptions.RequestException,
                          max_tries=retries,
                          max_time=300,
                          giveup=fatal_code,
                          jitter=backoff.random_jitter)
    def put(self, resource: str, data: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None):
        return requests.put(f"{self.api_url}/{resource}", data=data, headers=self.__merge_headers(headers))

    def __merge_headers(self, headers: Optional[Dict[str, str]] = None):
        if not headers:
            return self.headers
        else:
            merged = self.headers.copy()
            merged.update(**headers)
            return merged

    def is_20x(self, status: int):
        return status == 200 or status == 201 or status == 204


