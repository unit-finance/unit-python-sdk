import json
import requests
import backoff
from typing import Optional, Dict

from unit.utils.configuration import Configuration
from unit.models.codecs import UnitEncoder

get_max_retries = None
get_max_timeout = None


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
    def __init__(self, resource: str, configuration: Configuration):
        global get_max_timeout, get_max_retries

        self.resource = resource
        self.configuration = configuration
        get_max_timeout = configuration.get_timeout
        get_max_retries = configuration.get_retries

    @backoff.on_predicate(backoff.expo,
                          backoff_handler,
                          max_tries=get_max_retries,
                          max_time=get_max_timeout,
                          jitter=backoff.random_jitter)
    def get(self, resource: str, params: Dict = None, headers: Optional[Dict[str, str]] = None):
        return requests.get(f"{self.configuration.api_url}/{resource}", params=params, headers=self.__merge_headers(headers))

    @backoff.on_predicate(backoff.expo,
                          backoff_handler,
                          max_tries=get_max_retries,
                          max_time=get_max_timeout,
                          jitter=backoff.random_jitter)
    def post(self, resource: str, data: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None):
        data = json.dumps(data, cls=UnitEncoder) if data is not None else None
        return requests.post(f"{self.configuration.api_url}/{resource}", data=data, headers=self.__merge_headers(headers))

    @backoff.on_predicate(backoff.expo,
                          backoff_idempotency_key_handler,
                          max_tries=get_max_retries,
                          max_time=get_max_timeout,
                          jitter=backoff.random_jitter)
    def post_create(self, resource: str, data: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None):
        data = json.dumps(data, cls=UnitEncoder) if data is not None else None
        return requests.post(f"{self.configuration.api_url}/{resource}", data=data, headers=self.__merge_headers(headers))

    @backoff.on_predicate(backoff.expo,
                          backoff_handler,
                          max_tries=get_max_retries,
                          max_time=get_max_timeout,
                          jitter=backoff.random_jitter)
    def post_full_path(self, path: str, data: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None):
        data = json.dumps(data, cls=UnitEncoder) if data is not None else None
        return requests.post(path, data=data, headers=self.__merge_headers(headers))

    @backoff.on_predicate(backoff.expo,
                          backoff_handler,
                          max_tries=get_max_retries,
                          max_time=get_max_timeout,
                          jitter=backoff.random_jitter)
    def patch(self, resource: str, data: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None):
        data = json.dumps(data, cls=UnitEncoder) if data is not None else None
        return requests.patch(f"{self.configuration.api_url}/{resource}", data=data, headers=self.__merge_headers(headers))

    @backoff.on_predicate(backoff.expo,
                          backoff_handler,
                          max_tries=get_max_retries,
                          max_time=get_max_timeout,
                          jitter=backoff.random_jitter)
    def delete(self, resource: str, data: Dict = None, headers: Optional[Dict[str, str]] = None):
        data = json.dumps(data, cls=UnitEncoder) if data is not None else None
        return requests.delete(f"{self.configuration.api_url}/{resource}", data=data, headers=self.__merge_headers(headers))

    @backoff.on_predicate(backoff.expo,
                          backoff_handler,
                          max_tries=get_max_retries,
                          max_time=get_max_timeout,
                          jitter=backoff.random_jitter)
    def put(self, resource: str, data: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None):
        return requests.put(f"{self.configuration.api_url}/{resource}", data=data, headers=self.__merge_headers(headers))

    def __merge_headers(self, headers: Optional[Dict[str, str]] = None):
        if not headers:
            return self.configuration.get_headers()
        else:
            merged = self.configuration.get_headers().copy()
            merged.update(**headers)
            return merged

    @staticmethod
    def is_20x(status: int):
        return status == 200 or status == 201 or status == 204

