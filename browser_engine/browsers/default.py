from browser_engine.browsers.core.options import DefaultBrowserOptions
from browser_engine.browsers.core.request import BrowserRequestBase
from browser_engine.settings import SELENIUM_HOST
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options
import yaml
from extraction_engine import ExtractionEngine
import logging

logger = logging.getLogger(__name__)


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

    def delete_cookies(self):
        self.driver.delete_all_cookies()

    def close_browser(self):
        self.driver.quit()

    def update_viewport(self):
        if "x" in self.browser_options.viewport:
            w, h = self.browser_options.viewport.split("x")
            self.driver.set_window_size(w, h)

    def update_timeout(self):
        self.driver.set_page_load_timeout(self.timeout)

    def get_page(self):
        self.driver.get(self.url)

    def update_headers(self, ):
        if self.headers:
            cookies = self.headers.get("cookies", {})
            for cookie in cookies:
                if cookie.get("name") and cookie.get("value"):
                    self.driver.add_cookie(
                        {
                            'name': cookie['name'],
                            'value': cookie['value'],
                            # 'domain': cookie.get('domain')
                        }
                    )

    def extract_page_source(self):
        return self.driver.page_source

    def run_extractors(self, html=None):
        extraction_manifest = yaml.load(self.extractors, yaml.Loader)
        engine = ExtractionEngine(html=html, extraction_manifest=extraction_manifest)
        return engine.extract_data()

    def run_traversal_extractors(self, html=None):
        traversal_extraction_manifest = yaml.load(self.traversals, yaml.Loader)
        traversal_manifests = []
        for traversal in traversal_extraction_manifest:
            traversal['selector_id'] = traversal['traversal_id']
            traversal_manifest = {
                "extractor_id": traversal['traversal_id'],
                "extractor_type": "CustomContentExtractor",
                "data_selectors": [
                    traversal
                ]
            }
            traversal_manifests.append(traversal_manifest)
        engine = ExtractionEngine(html=html, extraction_manifest=traversal_manifests)
        traversal_data_raw = engine.extract_data()

        traversal_data = {}
        if traversal_data_raw is not None:
            for k, v in traversal_data_raw.items():
                traversal_data.update(v)

        return traversal_data

    def make_request(self):
        self.set_request_start()
        self.update_viewport()
        self.update_timeout()
        self.delete_cookies()
        self.get_page()

        if self.headers:
            self.update_headers()
            self.driver.refresh()
        is_simulation_success = False
        if self.simulation_code:
            simulate_fn = self.create_simulation_fn()
            if simulate_fn:
                try:
                    simulate_fn(self.driver)
                    is_simulation_success = True
                except Exception as e:
                    print("Simulation failed with error", e)
        html = self.extract_page_source()

        if self.extractors:
            extracted_data = self.run_extractors(html=html)
        else:
            extracted_data = None

        if self.traversals:
            traversals_data = self.run_traversal_extractors(html=html)
        else:
            traversals_data = None

        # all_cookies = self.driver.get_cookies()

        status_code = 200
        screen_shot = None
        if self.browser_options.take_screenshot is True:
            screen_shot = self.driver.get_screenshot_as_base64()
        content_length = len(html)
        all_cookies = self.driver.get_cookies()
        return html, status_code, screen_shot, content_length, all_cookies, \
               extracted_data, traversals_data, is_simulation_success


def create_browser_request(flask_request):
    url = flask_request.args.get('url')
    http_method = flask_request.args.get('http_method', 'get')
    take_screenshot = int(flask_request.args.get('take_screenshot', 0))
    browser_type = flask_request.args.get('browser_type', "chrome")
    viewport = flask_request.args.get('viewport', "1280x720")
    enable_images = flask_request.args.get('enable_images', 0)
    timeout = int(flask_request.args.get('timeout', 180))
    browser_options = DefaultBrowserOptions(
        enable_images=enable_images,
        take_screenshot=take_screenshot,
        viewport=viewport
    )
    json_data = flask_request.get_json() or {}
    headers = json_data.get("headers", None)
    if headers:
        headers = yaml.load(headers, yaml.Loader)

    simulation_code = json_data.get("simulation_code", None)
    extractors = json_data.get("extractors", None)
    traversals = json_data.get("traversals", None)
    return SeleniumBrowserRequest(url=url,
                                  timeout=timeout,
                                  http_method=http_method,
                                  browser_type=browser_type,
                                  headers=headers,
                                  extractors=extractors,
                                  traversals=traversals,
                                  simulation_code=simulation_code,
                                  browser_options=browser_options)
