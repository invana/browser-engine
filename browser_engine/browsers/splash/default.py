from browser_engine.browsers.core.request import BrowserRequestBase
from browser_engine.settings import BROWSER_HOST
from urllib.request import urlopen
import json


class SplashBrowserRequest(BrowserRequestBase):
    browser_type = "Splash"

    @staticmethod
    def generate_request_data(url_request=None):

        try:
            json_data = json.loads(url_request.read())
            html = json_data.get("html")
            status_code = url_request.getcode()
            screenshot = json_data.get("jpeg")
            content_length = len(html)
        except Exception as e:
            print(e)
            html = None
            status_code = None
            screenshot = None
            content_length = None

        cookies = {}
        return html, status_code, screenshot, content_length, cookies

    def make_request(self):
        self.set_request_start()
        url = "{}/render.json?url={}&timeout={}&html=1&jpeg={}&viewport={}".format(
            BROWSER_HOST, self.url,
            self.timeout,
            self.browser_options.enable_screenshot,
            self.browser_options.viewport,
        )
        print("==url", url)
        try:
            url_request = urlopen(url, timeout=self.timeout)
        except Exception as e:
            url_request = None
        return self.generate_request_data(url_request=url_request)
