import json
import requests


class ApiException(Exception):
    def __init__(self, api_response):
        self.err = f"""
            Error Code: {api_response.status_code}
            Error: {api_response.json()} 
            Headers: {api_response.headers}
        """
        super().__init__(self.err)


def _api_request_successful(response):
    if not str(response.status_code).startswith("2"):
        raise ApiException(response)


class ApiClient:
    def __init__(self):
        self._headers = {}

    def set_token(self, authorization_header):
        if self._headers:
            self._headers = {**self._headers, **authorization_header}
        self._headers = authorization_header

    def append_headers(self, headers_to_append):
        self._headers = {**self._headers, **headers_to_append}

    def get_headers(self):
        return self._headers

    def _api_request(self, method, url, headers=None, params=None, payload=None, return_json=True, files=None):
        response = requests.request(
            method=method,
            url=url,
            headers=headers if headers else self._headers,
            data=payload,
            files=files,
            params=params
        )

        _api_request_successful(response)
        if return_json:
            return response.json()
        else:
            return response

    def get_request(self, url, params=None, return_json=True):
        return self._api_request("get", url, params=params, return_json=return_json)

    def post_request(self, url, headers=None, params=None, payload=None, send_json=True, return_json=True):
        request_headers = {**self._headers, **{"Content-Type": "application/json"}} if send_json else self._headers
        return self._api_request(
            "post",
            url,
            headers={**request_headers, **headers} if headers else request_headers,
            params=params,
            payload=json.dumps(payload) if send_json else payload,
            return_json=return_json
        )

    def post_files(self, url, files, return_json=True):
        response = requests.post(
            files=files,
            url=url,
            headers=self._headers
        )
        _api_request_successful(response)
        if return_json:
            return response.json()
        else:
            return response

    def put_request(self, url, payload):
        self._headers = {**self._headers, **{"Content-Type": "application/json"}}
        return self._api_request("put", url, payload=json.dumps(payload))

    def post_content(self, url, request_headers, file):
        headers = {**self._headers, **request_headers}

        with open(file, "rb") as hdl:
            response = self._api_request(
                method="post",
                headers=headers,
                url=url,
                payload=hdl
                # files={'file': open(file, 'rb')}
            )
        return response