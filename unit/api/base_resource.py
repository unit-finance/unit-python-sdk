import json
import requests
import backoff
from typing import Optional, Dict
from unit.models.codecs import UnitEncoder

_retries = 1


def get_max_retries():
    return _retries


def backoff_idempotency_key_handler(e):
    return backoff_handler(e) and idempotency_key_is_present(e)


def backoff_handler(e):
    code = e.status_code
    return is_timeout(code) or is_rate_limit(code) or is_server_error(code)


def is_timeout(code):
    return code == 408


def is_rate_limit(code):
    return code == 429


def is_server_error(code):
    return 500 <= code <= 599


def idempotency_key_is_present(e):
    body = json.loads(e.request.body)
    if body is None:
        return False

    return body["data"]["attributes"].get("idempotencyKey") is not None


class BaseResource(object):
    def __init__(self, api_url, token, retries_amount):
        global _retries

        self.api_url = api_url.rstrip("/")
        self.token = token
        self.headers = {
            "content-type": "application/vnd.api+json",
            "authorization": f"Bearer {self.token}",
            "user-agent": "unit-python-sdk"
        }
        # max_tries must be greater than 0 due to an infinite loop of backoff library otherwise
        _retries = retries_amount if retries_amount > 1 else 1

    @backoff.on_predicate(backoff.expo,
                          backoff_handler,
                          max_tries=get_max_retries,
                          jitter=backoff.random_jitter)
    def get(self, resource: str, params: Dict = None, headers: Optional[Dict[str, str]] = None):
        return requests.get(f"{self.api_url}/{resource}", params=params, headers=self.__merge_headers(headers))

    @backoff.on_predicate(backoff.expo,
                          backoff_handler,
                          max_tries=get_max_retries,
                          jitter=backoff.random_jitter)
    def post(self, resource: str, data: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None):
        data = json.dumps(data, cls=UnitEncoder) if data is not None else None
        return requests.post(f"{self.api_url}/{resource}", data=data, headers=self.__merge_headers(headers))

    @backoff.on_predicate(backoff.expo,
                          backoff_idempotency_key_handler,
                          max_tries=get_max_retries,
                          jitter=backoff.random_jitter)
    def post_create(self, resource: str, data: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None):
        data = json.dumps(data, cls=UnitEncoder) if data is not None else None
        return requests.post(f"{self.api_url}/{resource}", data=data, headers=self.__merge_headers(headers))

    @backoff.on_predicate(backoff.expo,
                          backoff_handler,
                          max_tries=get_max_retries,
                          jitter=backoff.random_jitter)
    def patch(self, resource: str, data: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None):
        data = json.dumps(data, cls=UnitEncoder) if data is not None else None
        return requests.patch(f"{self.api_url}/{resource}", data=data, headers=self.__merge_headers(headers))

    @backoff.on_predicate(backoff.expo,
                          backoff_handler,
                          max_tries=get_max_retries,
                          jitter=backoff.random_jitter)
    def delete(self, resource: str, data: Dict = None, headers: Optional[Dict[str, str]] = None):
        data = json.dumps(data, cls=UnitEncoder) if data is not None else None
        return requests.delete(f"{self.api_url}/{resource}", data=data, headers=self.__merge_headers(headers))

    @backoff.on_predicate(backoff.expo,
                          backoff_handler,
                          max_tries=get_max_retries,
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
