from unit.app_config import sdk_version


class Configuration(object):
    def __init__(self, api_url, token, retries=1, timeout=120):
        self.api_url = self.__check_api_url(api_url)
        self.token = self.__check_token(token)
        self.retries = self.__check_retries(retries)
        self.timeout = self.__check_timeout(timeout)

    def get_headers(self):
        return {
            "content-type": "application/vnd.api+json",
            "authorization": f"Bearer {self.token}",
            "X-UNIT-SDK": f"unit-python-sdk@v{sdk_version}"
        }

    def set_api_url(self, api_url):
        self.api_url = self.__check_api_url(api_url)

    def set_token(self, token):
        self.token = self.__check_token(token)

    def set_timeout(self, timeout):
        self.timeout = self.__check_timeout(timeout)

    def set_retries(self, retries):
        self.retries = self.__check_retries(retries)

    def get_retries(self):
        return self.retries

    def get_api_url(self):
        return self.api_url

    def get_token(self):
        return self.token

    def get_timeout(self):
        return self.timeout

    @staticmethod
    def __check_timeout(seconds: int):
        if not seconds:
            raise Exception("timeout is missing")

        return seconds if seconds > 0 else 120

    @staticmethod
    def __check_retries(retries: int):
        if not retries:
            raise Exception("retries is missing")

        # max_tries must be greater than 0 due to an infinite loop of backoff library otherwise
        return retries if retries > 1 else 1

    @staticmethod
    def __check_api_url(api_url: str):
        if not api_url:
            raise Exception("api_url is missing")

        return api_url.rstrip("/")

    @staticmethod
    def __check_token(token: str):
        if not token or not token.startswith("v2"):
            raise Exception("token is missing")

        return token

