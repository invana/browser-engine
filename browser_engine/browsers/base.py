from browser_engine.default_settings import DEFAULT_USER_AGENT


class BrowserBase:
    """

    Usage:

        browser = URLLibBrowser()
        browser.request(url="https://invana.io", method="get")
        page = browser.read()
    """

    request_object = None

    def __init__(self, user_agent=None, proxy_ip=None, extra_headers=None
                 ):
        self.user_agent = user_agent or DEFAULT_USER_AGENT
        self.proxy_ip = proxy_ip
        self.extra_headers = extra_headers or {}

    def start_browser(self):
        raise NotImplementedError()

    def stop_browser(self):
        raise NotImplementedError()

    def construct_headers(self):
        return self.extra_headers

    def _request(self, method=None, url=None, data=None, headers=None):
        raise NotImplementedError()

    def request(self, method="get", url=None, data=None):
        headers = self.construct_headers()
        self.request_object = self._request(method=method.upper(), url=url, data=data, headers=headers)

    def get_screenshot(self):
        raise NotImplementedError()

    def refresh(self):
        raise NotImplementedError()

    def page_source(self):
        raise NotImplementedError()

    def __repr__(self):
        return "<{cls} user_agent={user_agent} proxy_ip={proxy_ip}>".format(
            cls=self.__class__.__name__,
            user_agent=self.user_agent,
            proxy_ip=self.proxy_ip
        )
