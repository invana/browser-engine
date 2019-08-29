from browser_engine.browsers.core.options import DefaultBrowserOptions
from datetime import datetime


class BrowserRequestBase(object):
    """



    """
    browser_type = "default"
    started_at = None

    def __init__(self,
                 url=None,
                 http_method=None,
                 browser_type="selenium",
                 timeout=30,
                 wait=0,
                 browser_options=None):
        self.url = url
        self.timeout = timeout
        self.wait = wait
        self.http_method = http_method
        self.browser_type = browser_type
        self.browser_options = browser_options

    def set_request_start(self):
        self.started_at = datetime.now()

    def get_request(self):
        return {
            "url": self.url,
            "http_method": self.http_method,
            "timeout": self.timeout,
            "wait": self.wait,
            "browser_type": self.browser_type,
            "browser_options": DefaultBrowserOptions().get_options(),
        }
