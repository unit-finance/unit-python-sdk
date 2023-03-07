
from unit.app_config import sdk_version

_retries = None
_timeout = None
_token = None
_api_url = None


class Configuration(object):
    def __init__(self, api_url, token, retries=1, timeout=120):
        self.api_url = api_url
        self.token = token
        self.retries = retries
        self.timeout = timeout

    def set_globals(self):
        global _timeout
        global _retries
        global _token
        global _api_url

        if not (_retries and _token and _api_url and _timeout):
            _api_url = self.api_url.rstrip("/")
            _token = self.token
            _retries = Configuration._check_retries(self.retries)
            _timeout = Configuration._check_timeout(self.timeout)

    @staticmethod
    def get_headers():
        return {
            "content-type": "application/vnd.api+json",
            "authorization": f"Bearer {_token}",
            "X-UNIT-SDK": f"unit-python-sdk@v{sdk_version}"
        }

    @staticmethod
    def set_token(retries=None):
        global _retries

        _retries = Configuration._check_retries(retries)
        return _retries

    @staticmethod
    def set_api_url(api_url):
        global _api_url
        _api_url = api_url
        return _api_url

    @staticmethod
    def set_token(token):
        global _token
        _token = token
        return _token

    @staticmethod
    def set_timeout(timeout=None):
        global _timeout

        _timeout = Configuration._check_timeout(timeout)
        return _timeout

    @staticmethod
    def get_retries():
        global _retries

        return _retries if _retries else Configuration.set_timeout()

    @staticmethod
    def get_api_url():
        global _api_url

        if _api_url:
            return _api_url

        else:
            raise ValueError

    @staticmethod
    def get_token():
        global _token

        if _token:
            return _token

        else:
            raise NotImplementedError

    @staticmethod
    def get_timeout():
        global _timeout

        return _timeout if _timeout else Configuration.set_timeout()

    @staticmethod
    def _check_timeout(timeout):
        return timeout if timeout > 0 else 120

    @staticmethod
    def _check_retries(retries):
        # max_tries must be greater than 0 due to an infinite loop of backoff library otherwise
        return retries if retries > 1 else 1


__all__ = [Configuration]

