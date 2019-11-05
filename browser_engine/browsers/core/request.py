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
                 extractors=None,
                 traversals=None,
                 form_data=None,
                 simulation_code=None,
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

        self.extractors = extractors
        self.traversals = traversals
        self.form_data = form_data
        self.simulation_code = simulation_code
        self.browser_options = browser_options

        self.simulation_fn = None

        self.driver = self.create_driver()

    def create_simulation_fn(self):
        d = {}
        try:
            exec(self.simulation_code.strip(), d)
            return d['simulate']
        except Exception as e:
            print("Failed to create simulation function with error", e)
            return None

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
