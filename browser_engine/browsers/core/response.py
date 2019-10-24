from .client import ClientDetail
import selenium
from selenium.common.exceptions import TimeoutException


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
        try:
            html, status_code, screenshot, content_length, all_cookies, \
            extracted_data, traversals_data, is_simulation_success = self.request.make_request()
            error_message = None
        except TimeoutException as e:
            print(e)
            html = None
            status_code = 999
            screenshot = None
            content_length = 0
            all_cookies = []  # TODO - get these cookies from driver directly.
            extracted_data = {}
            traversals_data = {}
            error_message = e.__str__()
            is_simulation_success = False
        self.request.close_browser()

        message = {
            "message": self.message,
            "client": ClientDetail(request=self.request).get_client_details(),
        }
        if self.request.url:
            message["request"] = self.request.get_request()
            message["response"] = {
                "status_code": status_code,
                "html": html,
                "extracted_data": extracted_data,
                "traversals_data": traversals_data,
                "is_simulation_success": is_simulation_success,
                "screenshot": screenshot,
                "content_length": content_length,
                "cookies": all_cookies,
                "error_message": error_message
            }

        return message


class DefaultBrowserResponse(BrowserResponseBase):
    pass
