import datetime
import httplib2
import urllib
import oauth2 as oauth
from urlparse import parse_qs, parse_qsl, urlparse


class Client(oauth.Client):
    """
    Custom client to support forcing Authorization header (which is required
    by LinkedIn). See http://github.com/brosner/python-oauth2/commit/82a05f96878f187f67c1af44befc1bec562e5c1f
    """

    def request(self, uri, method="GET", body=None, headers=None,
                redirections=httplib2.DEFAULT_MAX_REDIRECTS, connection_type=None,
                force_auth_header=False, parameters=None):

        DEFAULT_CONTENT_TYPE = "application/x-www-form-urlencoded"

        if not isinstance(headers, dict):
            headers = {}

        is_multipart = method == "POST" and headers.get("Content-Type", DEFAULT_CONTENT_TYPE) != DEFAULT_CONTENT_TYPE

        if body and method == "POST" and not is_multipart:
            parameters = parameters or {}
            parameters.update(dict(parse_qsl(body)))

        req = oauth.Request.from_consumer_and_token(self.consumer, token=self.token, http_method=method, http_url=uri,
                                                    parameters=parameters)

        req.sign_request(self.method, self.consumer, self.token)

        if force_auth_header:
            headers.update(req.to_header())

        if method == "POST":
            headers["Content-Type"] = headers.get("Content-Type", DEFAULT_CONTENT_TYPE)
            if is_multipart:
                headers.update(req.to_header())
            else:
                if not force_auth_header:
                    body = req.to_postdata()
                else:
                    body = urllib.urlencode(req.get_nonoauth_parameters(), True)
        elif method == "GET":
            if not force_auth_header:
                uri = req.to_url()
            elif parameters:
                uri = '%s?%s' % (req.normalized_url, urllib.urlencode(req.get_nonoauth_parameters(), True))
        else:
            if not force_auth_header:
                # don't call update twice.
                headers.update(req.to_header())

        return httplib2.Http.request(self, uri, method=method, body=body, headers=headers,
                                     redirections=redirections, connection_type=connection_type)


class OAuth20Token(object):
    def __init__(self, token, refresh_token=None, token_expiry=None):
        self.token = token
        self.refresh_token = refresh_token
        if token_expiry is not None:
            self.expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=token_expiry)
        else:
            self.expires = None

    def __str__(self):
        return str(self.token)
