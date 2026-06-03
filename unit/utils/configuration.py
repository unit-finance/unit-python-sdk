class Configuration(object):
    def __init__(self, api_url, token, retries=0, timeout=120, request_timeout=120):
        self.api_url = self.__check_api_url(api_url)
        self.token = self.__check_token(token)
        self.retries = self.__check_retries(retries)
        self.timeout = self.__check_timeout(timeout)
        self.request_timeout = self.__check_request_timeout(request_timeout)

    def get_headers(self):
        return {
            "content-type": "application/vnd.api+json",
            "authorization": f"Bearer {self.token}",
            "X-UNIT-SDK": f"unit-python-sdk@v1.3.0"
        }

    def set_api_url(self, api_url):
        self.api_url = self.__check_api_url(api_url)

    def set_token(self, token):
        self.token = self.__check_token(token)

    def set_timeout(self, timeout):
        self.timeout = self.__check_timeout(timeout)

    def set_request_timeout(self, request_timeout):
        self.request_timeout = self.__check_request_timeout(request_timeout)

    def set_retries(self, retries):
        self.retries = self.__check_retries(retries)

    def get_tries(self):
        return self.retries + 1

    def get_api_url(self):
        return self.api_url

    def get_token(self):
        return self.token

    def get_timeout(self):
        return self.timeout

    def get_request_timeout(self):
        return self.request_timeout

    @staticmethod
    def __check_timeout(seconds):
        try:
            i_seconds = int(seconds)

        except Exception as e:
            raise Exception("seconds must be an int")

        if i_seconds < 0:
            raise Exception("seconds must be 0 or greater")

        return i_seconds

    @staticmethod
    def __check_request_timeout(seconds):
        # Per-request HTTP timeout passed to requests. Must be a positive int;
        # None is rejected to avoid waiting indefinitely; 0 is rejected to avoid immediate timeouts.
        if seconds is None:
            raise Exception("request_timeout must be a positive int")

        try:
            i_seconds = int(seconds)
        except Exception:
            raise Exception("request_timeout must be a positive int")

        if i_seconds <= 0:
            raise Exception("request_timeout must be a positive int")

        return i_seconds

    @staticmethod
    def __check_retries(retries):
        try:
            i_retries = int(retries)

        except Exception as e:
            raise Exception("retries must be an int")

        if i_retries < 0:
            raise Exception("retries must be 0 or greater")

        return i_retries

    @staticmethod
    def __check_api_url(api_url: str):
        if not api_url:
            raise Exception("api_url is missing")

        return api_url.rstrip("/")

    @staticmethod
    def __check_token(token: str):
        if not token:
            raise Exception("token is missing")

        return token
