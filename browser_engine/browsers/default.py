from browser_engine.browsers.core.options import DefaultBrowserOptions
from browser_engine.browsers.core.request import BrowserRequestBase
from browser_engine.settings import SELENIUM_HOST, BROWSER_TYPE
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType


class SeleniumBrowserRequestBase(BrowserRequestBase):
    browser_type = "Selenium"

    def create_driver(self):
        capabilities = webdriver.DesiredCapabilities.CHROME

        proxy_address = self.headers.get("proxy")
        if proxy_address:
            proxy = Proxy({
                'proxyType': ProxyType.MANUAL,
                'httpProxy': proxy_address,
                'ftpProxy': proxy_address,
                'sslProxy': proxy_address,
                'noProxy': ''})
        else:
            proxy = None
            # proxy.add_to_capabilities(capabilities)
        # print ("Proxy", proxy)
        driver = webdriver.Remote(
            command_executor='{}/wd/hub'.format(SELENIUM_HOST),
            desired_capabilities=capabilities,
            proxy=proxy
        )

        return driver

    def delete_cookies(self, driver=None):
        driver.delete_all_cookies()

    def update_viewport(self, driver=None):
        if "x" in self.browser_options.viewport:
            w, h = self.browser_options.viewport.split("x")
            driver.set_window_size(w, h)

    def update_timeout(self, driver=None):
        driver.set_page_load_timeout(self.timeout)

    def get_page(self, driver=None):
        driver.get(self.url)

    def update_headers(self, driver=None):
        if self.headers:
            cookies = self.headers.get("cookies", {})
            for cookie in cookies:
                if cookie.get("name") and cookie.get("value"):
                    driver.add_cookie(
                        {'name': cookie['name'], 'value': cookie['value'], 'domain': cookie.get('domain')})

    def close_browser(self, driver=None):
        driver.close()

    def make_request(self):
        self.set_request_start()
        driver = self.create_driver()
        self.update_viewport(driver=driver)
        self.delete_cookies(driver=driver)
        self.get_page(driver=driver)
        self.update_headers(driver=driver)
        driver.refresh()
        html = driver.page_source
        all_cookies = driver.get_cookies()

        status_code = 200
        if self.browser_options.enable_screenshot is False:
            screenshot = None
        else:
            screenshot = driver.get_screenshot_as_base64()
        content_length = len(html)
        all_cookies = driver.get_cookies()
        self.close_browser(driver=driver)
        return html, status_code, screenshot, content_length, all_cookies


class SeleniumChromeBrowserRequest(SeleniumBrowserRequestBase):
    pass


class SeleniumUnitHTMLBrowserRequest(SeleniumBrowserRequestBase):
    pass


def create_browser_request(flask_request):
    url = flask_request.args.get('url')
    http_method = flask_request.args.get('http_method', 'get')
    browser_type = flask_request.args.get('browser_type', 'chrome')
    enable_screenshot = flask_request.args.get('enable_screenshot', 0)
    viewport = flask_request.args.get('viewport', "1280x720")
    enable_images = flask_request.args.get('enable_images', 0)
    browser_options = DefaultBrowserOptions(enable_images=enable_images,
                                            enable_screenshot=enable_screenshot,
                                            viewport=viewport)
    headers = flask_request.get_json()
    browser_klass = SeleniumChromeBrowserRequest
    return browser_klass(url=url,
                         http_method=http_method,
                         browser_type=browser_type,
                         headers=headers.get("headers", {}),
                         browser_options=browser_options)
