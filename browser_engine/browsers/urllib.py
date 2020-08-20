from .base import BrowserBase
from urllib.request import urlopen, Request
from urllib.error import URLError
import logging
from browser_engine.default_settings import DEFAULT_BROWSER_TIMEOUT, DEFAULT_USER_AGENT

logger = logging.getLogger(__name__)


class URLLibBrowser(BrowserBase):
    html_source = None  # tmp variable to hold page_source info; this w

    def _request(self, method=None, url=None, data=None, headers=None):

        if self.user_agent:
            headers['User-agent'] = self.user_agent

        req = Request(url, method=method, headers=headers)
        if self.proxy_ip:
            proxy_type = "http" if self.proxy_ip.startswith("http://") else "https"
            req.set_proxy(proxy_type.split("://")[1], proxy_type)
        try:
            return urlopen(req, timeout=DEFAULT_BROWSER_TIMEOUT)
        except URLError as e:
            logger.error("Unable to open\n\n%s\n\ndue to the error\n\n%s\n\n" % (url, e))
            return None

    def start_browser(self):
        pass

    def stop_browser(self):
        pass

    def page_source(self):
        if self.request_object and self.html_source is None:
            self.html_source = self.request_object.read().decode("utf-8")
        return self.html_source

    def get_screenshot(self):
        return None

    def get_cookies(self):
        return None

    def refresh(self):
        pass
