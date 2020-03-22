from browser_engine.default_settings import DEFAULT_USER_AGENT
from .settings import DefaultBrowserSettings
from datetime import datetime


class BrowserBase:
    """

    Usage:

        browser = URLLibBrowser()
        browser.load_page(url="https://invana.io", method="get")
        page = browser.read()
    """

    request_object = None

    def __init__(self, user_agent=None, proxy_ip=None, headers=None, browser_settings=None):
        self.user_agent = user_agent or DEFAULT_USER_AGENT
        self.proxy_ip = proxy_ip
        self.headers = headers or {}
        self.started_at = datetime.now()
        self.browser_settings = DefaultBrowserSettings(options=browser_settings)

    def construct_headers(self):
        # TODO - add proxy here
        # TODO - add user agent here
        return self.headers

    def _request(self, method=None, url=None, data=None, headers=None):
        raise NotImplementedError()

    def load_page(self, method="get", url=None, data=None):
        headers = self.construct_headers()
        self.request_object = self._request(method=method.upper(), url=url, data=data, headers=headers)

    def start_browser(self):
        raise NotImplementedError()

    def stop_browser(self):
        raise NotImplementedError()

    def get_screenshot(self):
        raise NotImplementedError()

    def refresh(self):
        raise NotImplementedError()

    def page_source(self):
        raise NotImplementedError()

    def get_cookies():
        raise NotImplementedError()

    def __repr__(self):
        return "<{cls} user_agent={user_agent} proxy_ip={proxy_ip}>".format(
            cls=self.__class__.__name__,
            user_agent=self.user_agent,
            proxy_ip=self.proxy_ip
        )
