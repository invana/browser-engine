from .client import ClientDetail


class BrowserResponseBase(object):

    def __init__(self,
                 message=None,
                 request=None,
                 client_details=None
                 ):
        self.message = message
        self.request = request
        self.client_details = client_details

    def get_response(self):
        html, status_code, screenshot, content_length, all_cookies = self.request.make_request()
        message = {
            "message": self.message,
            "client": ClientDetail(request=self.request).get_client_details(),
        }
        if self.request.url:
            message["request"] = self.request.get_request()
            message["response"] = {
                "status_code": status_code,
                "html": html,
                "screenshot": screenshot,
                "content_length": content_length,
                "cookies": all_cookies
            }

        return message


class DefaultBrowserResponse(BrowserResponseBase):
    pass
