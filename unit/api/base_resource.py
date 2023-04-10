import json
import requests
import backoff
from typing import Optional, Dict

from unit.utils.configuration import Configuration
from unit.models.codecs import UnitEncoder


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
        self.resource = resource
        self.configuration = configuration

    def get(self, resource: str, params: Dict = None, headers: Optional[Dict[str, str]] = None):

        @backoff.on_predicate(backoff.expo,
                              backoff_handler,
                              max_tries=self.configuration.get_tries,
                              max_time=self.configuration.get_timeout,
                              jitter=backoff.random_jitter)
        def get_with_backoff(path: str, p: Dict, h: Dict[str, str]):
            return requests.get(path, params=p, headers=h)

        return get_with_backoff(f"{self.configuration.api_url}/{resource}", params, self.__merge_headers(headers))

    def post(self, resource: str, data: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None):
        data = json.dumps(data, cls=UnitEncoder) if data is not None else None

        @backoff.on_predicate(backoff.expo,
                              backoff_handler,
                              max_tries=self.configuration.get_tries,
                              max_time=self.configuration.get_timeout,
                              jitter=backoff.random_jitter)
        def post_with_backoff(path: str, d: Dict, h: Dict[str, str]):
            return requests.post(path, data=d, headers=h)

        return post_with_backoff(f"{self.configuration.api_url}/{resource}", data, self.__merge_headers(headers))

    def post_create(self, resource: str, data: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None):
        data = json.dumps(data, cls=UnitEncoder) if data is not None else None

        @backoff.on_predicate(backoff.expo,
                              backoff_idempotency_key_handler,
                              max_tries=self.configuration.get_tries,
                              max_time=self.configuration.get_timeout,
                              jitter=backoff.random_jitter)
        def post_create_with_backoff(path: str, d, h):
            return requests.post(path, data=d, headers=h)

        return post_create_with_backoff(f"{self.configuration.api_url}/{resource}", data, self.__merge_headers(headers))

    def post_full_path(self, path: str, data: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None):
        data = json.dumps(data, cls=UnitEncoder) if data is not None else None

        @backoff.on_predicate(backoff.expo,
                              backoff_handler,
                              max_tries=self.configuration.get_tries,
                              max_time=self.configuration.get_timeout,
                              jitter=backoff.random_jitter)
        def post_full_path_with_backoff(p, d, h):
            return requests.post(p, data=d, headers=h)

        return post_full_path_with_backoff(path, data, self.__merge_headers(headers))

    def patch(self, resource: str, data: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None):
        data = json.dumps(data, cls=UnitEncoder) if data is not None else None

        @backoff.on_predicate(backoff.expo,
                              backoff_handler,
                              max_tries=self.configuration.get_tries,
                              max_time=self.configuration.get_timeout,
                              jitter=backoff.random_jitter)
        def patch_with_backoff(p, d, h):
            return requests.patch(p, data=d, headers=h)

        return patch_with_backoff(f"{self.configuration.api_url}/{resource}", data, self.__merge_headers(headers))

    def delete(self, resource: str, data: Dict = None, headers: Optional[Dict[str, str]] = None):
        data = json.dumps(data, cls=UnitEncoder) if data is not None else None

        @backoff.on_predicate(backoff.expo,
                              backoff_handler,
                              max_tries=self.configuration.get_tries,
                              max_time=self.configuration.get_timeout,
                              jitter=backoff.random_jitter)
        def delete_with_backoff(p, d, h):
            return requests.delete(p, data=d, headers=h)

        return delete_with_backoff(f"{self.configuration.api_url}/{resource}", data, self.__merge_headers(headers))

    def put(self, resource: str, data: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None):
        @backoff.on_predicate(backoff.expo,
                              backoff_handler,
                              max_tries=self.configuration.get_tries,
                              max_time=self.configuration.get_timeout,
                              jitter=backoff.random_jitter)
        def put_with_backoff(p, d, h):
            return requests.put(p, data=d, headers=h)

        return put_with_backoff(f"{self.configuration.api_url}/{resource}", data, self.__merge_headers(headers))

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

