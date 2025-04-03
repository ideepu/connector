import json
from copy import copy
from typing import Any

import requests

from src.config import config
from src.exception import BaseRequestException, RequestMethodNotAllowed
from src.libs.status_code import HttpStatusCode


class BaseRequest:
    request_base_url: str = config.BASE_URL
    request_supported_methods: list[str] = ['GET, POST', 'PUT', 'DELETE']
    request_headers: dict[str, str] = {'authorization': config.API_KEY.get_secret_value()}
    request_params: dict[str, Any] = {}
    request_log_response_codes: list[int] = [HttpStatusCode.INTERNAL_SERVER_ERROR]

    def __init__(
        self,
        base_url: str,
        supported_methods: list[str] = None,
        headers: dict[str, str] = None,
        log_response_codes: list[int] = None,
    ):
        if supported_methods:
            self.request_supported_methods = supported_methods

        self.request_base_url = base_url

        if headers:
            self.request_headers.update(headers)

        if log_response_codes:
            self.request_log_response_codes = log_response_codes

    def _request(
        self,
        method: str,
        url_path: str = '',
        data: Any = None,
        params: dict[str, Any] = None,
        **kwargs: dict,
    ) -> dict:
        if method not in self.request_supported_methods:
            raise RequestMethodNotAllowed(f'Methods allowed: {self.request_supported_methods}')

        method = method.lower()
        url = f'{self.request_base_url}{url_path}'

        if data:
            data = json.dumps(data)

        # Shallow copy to avoid changing the params in the same context
        request_params = copy(self.request_params)
        if params:
            request_params.update(params)

        headers = copy(self.request_headers)
        headers.update(kwargs.get('headers', {}))
        kwargs['headers'] = headers
        response: requests.Response = getattr(requests, method)(url=url, data=data, params=request_params, **kwargs)

        if self.request_log_response_codes and response.status_code in self.request_log_response_codes:
            raise BaseRequestException(
                message=f'Request failed: Request returned {response.status_code} with the text {response.text} against {method} {url}',
                status_code=response.status_code,
            )

        try:
            return response.json()
        except Exception as e:
            raise BaseRequestException(
                message=f'Failed to parse response: {response.text}',
                status_code=response.status_code,
            ) from e

    def get(self, url, params=None, **kwargs):
        return self._request(method='GET', url_path=url, params=params, **kwargs)
