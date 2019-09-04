from browser_engine.browsers.core.options import DefaultBrowserOptions
from datetime import datetime


class BrowserRequestBase(object):
    """



    """
    started_at = None

    def __init__(self,
                 url=None,
                 http_method=None,
                 timeout=30,
                 browser_type=None,
                 wait=0,
                 headers=None,
                 browser_options=None):
        self.url = url
        self.timeout = timeout
        self.browser_type = browser_type
        self.wait = wait
        self.http_method = http_method
        if headers:
            self.headers = {k.lower(): v for k, v in headers.items()}
        else:
            self.headers = {}

        self.browser_options = browser_options

    def set_request_start(self):
        self.started_at = datetime.now()

    def get_request(self):
        return {
            "url": self.url,
            "http_method": self.http_method,
            "timeout": self.timeout,
            "wait": self.wait,
            "headers": self.headers,
            "browser_options": self.browser_options.get_options(),
        }
