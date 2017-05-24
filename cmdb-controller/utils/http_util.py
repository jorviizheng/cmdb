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


@coroutine
def http_cookie(url):
    task_user_name = 'task_user'
    task_user_password = 'MTIzMTIz'
    url = '%s/api/async/v1/user/login' % url
    try:
        client = AsyncHTTPClient()
        post_data = {
            "user_name": task_user_name,
            "user_password": task_user_password
        }

        headers = HTTPHeaders()
        headers.add('Content-Type', 'application/json')
        headers.add('User-Name', task_user_name)

        response = yield client.fetch(
            url,
            method='POST',
            headers=headers,
            body=json_encode(post_data),
            validate_cert=False,
            request_timeout=100
        )
        cookie = response.headers["Set-cookie"]
        raise Return(cookie)

    except HTTPError as error:
        raise error

