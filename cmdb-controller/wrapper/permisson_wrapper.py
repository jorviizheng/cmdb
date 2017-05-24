from tornado.httpclient import HTTPClient
from tornado.httputil import HTTPHeaders
from tornado.escape import json_encode

API_URL = "http://cmdb.wanda.cn"


def permisson(function):
    def _permisson(self):
        try:
            flag = self.user_name
            if flag == 'admin':
                res = function(self)
                return res
            else:
                return 403
        except Exception as e:
            # Other errors are possible, such as IOError.
            print("Error: " + str(e))

    return _permisson            
