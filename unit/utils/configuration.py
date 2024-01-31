class Configuration(object):
    def __init__(self, api_url, token, retries=0, timeout=120):
        self.api_url = self.__check_api_url(api_url)
        self.token = self.__check_token(token)
        self.retries = self.__check_retries(retries)
        self.timeout = self.__check_timeout(timeout)

    def get_headers(self):
        return {
            "content-type": "application/vnd.api+json",
            "authorization": f"Bearer {self.token}",
            "X-UNIT-SDK": f"unit-python-sdk@v0.30.0"
        }

    def set_api_url(self, api_url):
        self.api_url = self.__check_api_url(api_url)

    def set_token(self, token):
        self.token = self.__check_token(token)

    def set_timeout(self, timeout):
        self.timeout = self.__check_timeout(timeout)

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

