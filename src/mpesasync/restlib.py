import enum
from typing import Any

import httpx
import ujson
from pydantic import BaseModel

from mpesasync.contracts import MpesaError, MpesaResponse


class HttpMethod(enum.Enum):
    post = "post"
    get = "get"
    put = "put"


class HttpClient(BaseModel):
    """
    Handles making http requests
    """

    @classmethod
    async def HttpPost(cls, url, data, access_token=None, params=None, **kwargs):
        resp = await cls.async_http_request(url, data, HttpMethod.post, access_token, params, **kwargs)
        return resp

    @classmethod
    async def HttpGet(cls, url, data=None, access_token=None, params=None, **kwargs):
        resp = await cls.async_http_request(url, data, HttpMethod.get, access_token, params, **kwargs)
        return resp

    @classmethod
    async def HttpPut(cls, url, data, access_token=None, params=None, **kwargs):
        resp = await cls.async_http_request(url, data, HttpMethod.put, access_token, params, **kwargs)
        return resp

    @classmethod
    async def async_http_request(cls, url: str, data: dict, method: HttpMethod, access_token: str, params, **kwargs) -> \
            MpesaResponse[
                Any]:
        resp = None
        if access_token is not None:
            _headers = {
                "Content-Type": "Application/Json",
                "Authorization": "Bearer %s" % access_token
            }
        else:
            _headers = None
        if data is not None:
            data = ujson.dumps(data)
        async with httpx.AsyncClient(timeout=kwargs.get("timeout", 100.0)) as client:
            if method == method.post:
                resp = await client.post(url, headers=_headers, data=data, params=params, **kwargs)
            if method == method.get:
                resp = await client.get(url, headers=_headers, params=params, **kwargs)
            if method == method.put:
                resp = await client.put(url, headers=_headers, data=data, params=params, **kwargs)
        if resp is None:
            raise ValueError("Unsupported request method %s" % method.value)

        # check for errors
        if resp.status_code < 299:
            return MpesaResponse[Any](data=resp.json())
        else:
            try:
                error = MpesaError.parse_obj(resp.json())
            except Exception as exc:
                error = MpesaError(
                    requestId="",
                    errorCode=resp.status_code,
                    errorMessage=resp.text
                )
            return MpesaResponse[dict](error=error)
