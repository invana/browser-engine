from browser_engine.default_settings import SELENIUM_HOST as DEFAULT_SELENIUM_HOST
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options
import logging
from browser_engine.default_settings import BROWSER_TYPE
from datetime import datetime

logger = logging.getLogger(__name__)


class DefaultBrowserSettings(object):
    """

    options = {
        "load_images" : false,
        "enable_adblocker": false,
        "viewport": "1280x720",
        "timeout": 180
    }
    """
    viewport = "1280x720"
    enable_adblocker = False
    load_images = False
    timeout = 180
    browser_type = "CHROME"
    SELENIUM_HOST = DEFAULT_SELENIUM_HOST

    def __init__(self, options=None):
        if options is not None:
            for k, v in options.items():
                setattr(self, k, v)

    def get_settings(self):
        settings = {}
        for key in self.__dict__.keys():
            settings[key] = getattr(self, key)
        return settings


class SeleniumBrowser:

    def __init__(self, url=None, method=None, headers=None,
                 browser_settings=None, request=None):
        self.url = url
        self.method = method
        self.headers = headers or {}
        self.request = request
        self.browser_settings = DefaultBrowserSettings(options=browser_settings)
        self.driver = self.create_driver()
        self.started_at = datetime.now()

    def get_request(self):
        return {
            "url": self.url,
            "http_method": self.method,
            "browser_settings": self.browser_settings,
            "headers": self.headers,
            "browser_options": self.browser_settings.get_settings(),
        }

    def clear_cookies(self):
        self.driver.delete_all_cookies()

    def close_browser(self):
        self.driver.quit()

    def update_viewport(self):
        if "x" in self.browser_settings.viewport:
            w, h = self.browser_settings.viewport.split("x")
            # self.driver.set_window_position(0, 0)
            self.driver.set_window_size(w, h)

    def update_timeout(self):
        self.driver.set_page_load_timeout(self.browser_settings.timeout)

    def get_page(self):
        self.driver.get(self.url)

    def refresh_browser(self):
        self.driver.refresh()

    def update_headers(self, ):
        if self.headers:
            self.clear_cookies()
            cookies = self.headers.get("cookies", {})
            for cookie in cookies:
                if cookie.get("name") and cookie.get("value"):
                    if "expiry" in cookie:
                        del cookie['expiry']
                    logger.debug("Adding the cookie", cookie)
                    self.driver.add_cookie(
                        cookie
                    )
            self.refresh_browser()

    def page_source(self):
        return self.driver.page_source

    def get_screenshot(self):
        return self.driver.get_screenshot_as_base64()

    def get_element(self, selector=None, parent_element=None):

        parent_element = parent_element or self.driver
        selector_type = selector.get("selector_type", "css")
        index_number = selector.get("index_number", 0)
        try:
            if selector_type == "css":
                return parent_element.find_element_by_css_selector(selector.get("selector"))
            elif selector_type == "name":
                return parent_element.find_element_by_name(selector.get("selector"))
            elif selector_type == "xpath":
                return parent_element.find_element_by_xpath(selector.get("selector"))
            else:
                raise Exception("selector_type cannot be None. Possible options css or name or xpath ")
        except Exception as e:
            logger.error(e)

    def create_driver(self):

        if BROWSER_TYPE.lower() == "selenium-chrome":
            capabilities = webdriver.DesiredCapabilities.CHROME
        elif BROWSER_TYPE.lower() == "selenium-firefox":
            capabilities = webdriver.DesiredCapabilities.FIREFOX
        elif BROWSER_TYPE.lower() == "selenium-htmlunit":
            capabilities = webdriver.DesiredCapabilities.HTMLUNIT
        elif BROWSER_TYPE.lower() == "selenium-htmlunitwithjs":
            capabilities = webdriver.DesiredCapabilities.HTMLUNITWITHJS
        else:
            raise NotImplementedError()

        proxy_address = self.headers.get("proxy")
        if proxy_address:
            proxy = Proxy(
                {
                    'proxyType': ProxyType.MANUAL,
                    'httpProxy': proxy_address,
                    'ftpProxy': proxy_address,
                    'sslProxy': proxy_address,
                    'noProxy': ''
                }
            )
        else:
            proxy = None

        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--start-fullscreen")

        """
        # optional arguments 
        # options.add_argument("--window-position=0,0")
        # options.add_argument('--headless')
        """
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        user_agent = self.headers.get("user-agent")
        if user_agent:
            options.add_argument("user-agent={}".format(user_agent))

        driver = webdriver.Remote(
            command_executor='{}/wd/hub'.format(self.browser_settings.SELENIUM_HOST),
            desired_capabilities=capabilities,
            proxy=proxy,
            options=options
        )
        return driver

    def start(self):
        self.update_viewport()
        self.update_timeout()
        self.clear_cookies()
        self.get_page()

        if self.headers:
            self.update_headers()
