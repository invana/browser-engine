from browser_engine.browsers.core.options import DefaultBrowserOptions
from browser_engine.browsers.core.request import BrowserRequestBase
from browser_engine.settings import SELENIUM_HOST
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options
import yaml
from extraction_engine import ExtractionEngine


class SeleniumBrowserRequest(BrowserRequestBase):

    def create_driver(self):
        selenium_browser_type = self.browser_type
        if selenium_browser_type == "chrome":
            capabilities = webdriver.DesiredCapabilities.CHROME
        elif selenium_browser_type == "firefox":
            capabilities = webdriver.DesiredCapabilities.FIREFOX
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
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        user_agent = self.headers.get("user-agent")
        if user_agent:
            options.add_argument("user-agent={}".format(user_agent))

        driver = webdriver.Remote(
            command_executor='{}/wd/hub'.format(SELENIUM_HOST),
            desired_capabilities=capabilities,
            proxy=proxy,
            options=options
        )

        return driver

    @staticmethod
    def delete_cookies(driver=None):
        driver.delete_all_cookies()

    @staticmethod
    def close_browser(driver=None):
        driver.quit()

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
                        {
                            'name': cookie['name'],
                            'value': cookie['value'],
                            # 'domain': cookie.get('domain')
                        }
                    )

    @staticmethod
    def extract_page_source(driver=None):
        return driver.page_source

    def run_extractors(self, html=None):
        extraction_manifest = yaml.load(self.extractors, yaml.Loader)
        engine = ExtractionEngine(html=html, extraction_manifest=extraction_manifest)
        return engine.extract_data()

    def make_request(self):
        self.set_request_start()
        driver = self.create_driver()
        self.update_viewport(driver=driver)
        self.update_timeout(driver=driver)
        self.delete_cookies(driver=driver)
        self.get_page(driver=driver)
        if self.headers:
            self.update_headers(driver=driver)
            driver.refresh()
        html = self.extract_page_source(driver=driver)

        if self.extractors:
            extracted_data = self.run_extractors(html=html)
        else:
            extracted_data = None

        # all_cookies = driver.get_cookies()

        status_code = 200
        screen_shot = None
        if self.browser_options.take_screenshot is True:
            screen_shot = driver.get_screenshot_as_base64()
        content_length = len(html)
        all_cookies = driver.get_cookies()
        self.close_browser(driver=driver)
        return html, status_code, screen_shot, content_length, all_cookies, extracted_data


def create_browser_request(flask_request):
    url = flask_request.args.get('url')
    http_method = flask_request.args.get('http_method', 'get')
    take_screenshot = int(flask_request.args.get('take_screenshot', 0))
    browser_type = flask_request.args.get('browser_type', "chrome")
    viewport = flask_request.args.get('viewport', "1280x720")
    enable_images = flask_request.args.get('enable_images', 0)
    browser_options = DefaultBrowserOptions(
        enable_images=enable_images,
        take_screenshot=take_screenshot,
        viewport=viewport
    )
    json_data = flask_request.get_json()
    headers = json_data.get("headers", {})
    extractors = json_data.get("extractors", None)
    return SeleniumBrowserRequest(url=url,
                                  http_method=http_method,
                                  browser_type=browser_type,
                                  headers=headers,
                                  extractors=extractors,
                                  browser_options=browser_options)
