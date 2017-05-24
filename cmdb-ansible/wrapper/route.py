from tornado.web import RequestHandler, HTTPError
import functools


def route(url_pattern):

    def handler_wapper(cls):
        assert(issubclass(cls, RequestHandler))
        cls.url_pattern = url_pattern
        return cls
    return handler_wapper

def authenticated(method):
    """Decorate methods with this to require that the user be logged in.

    If the user is not logged in, they will be redirected to the configured
    `login url <RequestHandler.get_login_url>`.

    If you configure a login url with a query parameter, Tornado will
    assume you know what you're doing and use it as-is.  If not, it
    will add a `next` parameter so the login page knows where to send
    you once you're logged in.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            if self.request.method in ("GET", "HEAD"):
                url = self.get_login_url()
                if 'domain' in self.application.settings:
                    domain = self.application.settings["domain"]
                else:
                    domain = self.request.host
                next_url = 'http://' + domain + '/' + url
                self.redirect(next_url)
                return
            raise HTTPError(403)
        return method(self, *args, **kwargs)
    return wrapper