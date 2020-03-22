from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options
import logging
from browser_engine.default_settings import DEFAULT_BROWSER_TYPE
from .base import BrowserBase

logger = logging.getLogger(__name__)


class SeleniumBrowser(BrowserBase):

    def __init__(self, user_agent=None, proxy_ip=None, headers=None, browser_settings=None):
        super(SeleniumBrowser, self).__init__(user_agent=user_agent, proxy_ip=proxy_ip, headers=headers,
                                              browser_settings=browser_settings)

        self.driver = self.create_driver()

    def get_request(self):
        return {
            # "url": self.url,
            # "http_method": self.method,
            "browser_settings": self.browser_settings,
            "headers": self.headers,
            "browser_options": self.browser_settings.get_settings(),
        }

    def clear_cookies(self):
        self.driver.delete_all_cookies()

    def get_cookies(self):
        return self.driver.get_cookies()

    def stop_browser(self):
        self.driver.quit()

    def update_viewport(self):
        if "x" in self.browser_settings.viewport:
            w, h = self.browser_settings.viewport.split("x")
            # self.driver.set_window_position(0, 0)
            self.driver.set_window_size(w, h)

    def update_timeout(self):
        self.driver.set_page_load_timeout(self.browser_settings.timeout)

    def load_page(self, method="get", url=None, data=None):
        self.driver.get(url)

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

        if DEFAULT_BROWSER_TYPE.lower() == "selenium-chrome":
            capabilities = webdriver.DesiredCapabilities.CHROME
        elif DEFAULT_BROWSER_TYPE.lower() == "selenium-firefox":
            capabilities = webdriver.DesiredCapabilities.FIREFOX
        elif DEFAULT_BROWSER_TYPE.lower() == "selenium-htmlunit":
            capabilities = webdriver.DesiredCapabilities.HTMLUNIT
        elif DEFAULT_BROWSER_TYPE.lower() == "selenium-htmlunitwithjs":
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
            command_executor='{}/wd/hub'.format(self.browser_settings.selenium_host),
            desired_capabilities=capabilities,
            proxy=proxy,
            options=options
        )
        return driver

    def start_browser(self):
        self.update_viewport()
        self.update_timeout()
        self.clear_cookies()
        if self.headers:
            self.update_headers()
        # self.load_page()
