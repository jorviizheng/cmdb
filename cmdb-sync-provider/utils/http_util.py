from __future__ import print_function
from tornado.httpclient import AsyncHTTPClient,HTTPError,HTTPRequest
from tornado.httputil import HTTPHeaders
from tornado.gen import coroutine,Return
from tornado.escape import json_encode

@coroutine
def http_client(url, method, cookie, body=None, time_out=None):
        client = AsyncHTTPClient()
        headers = HTTPHeaders()
        headers.add('Content-Type','application/json')
        if cookie:
            headers.add('Cookie', cookie)

        if body:
            body = json_encode(body)

        if time_out:
            request = HTTPRequest(url, headers=headers, method=method, validate_cert=False, body=body,
                                  request_timeout=time_out)
        else:
            request = HTTPRequest(url,headers=headers,method=method,validate_cert=False,body=body)

        try:
            response = yield client.fetch(request)
        except HTTPError as error:
            raise error
        else:
            raise Return(response)


