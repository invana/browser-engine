from browser_engine.browsers.core.request import BrowserRequestBase
from browser_engine.settings import BROWSER_HOST, BROWSER_TYPE
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

if BROWSER_TYPE == "selenium":
    driver = webdriver.Remote(command_executor='{}/wd/hub'.format(BROWSER_HOST),
                              desired_capabilities=DesiredCapabilities.CHROME)


class SeleniumBrowserRequestBase(BrowserRequestBase):
    browser_type = "Selenium"

    def make_request(self):
        self.set_request_start()
        if "x" in self.browser_options.viewport:
            w, h = self.browser_options.viewport.split("x")
            driver.set_window_size(w, h)
        driver.set_page_load_timeout(self.timeout)
        driver.get(self.url)
        html = driver.page_source
        status_code = 200
        if self.browser_options.enable_screenshot is False:
            screenshot = None
        else:
            screenshot = driver.get_screenshot_as_base64()
        content_length = len(html)
        all_cookies = driver.get_cookies()
        return html, status_code, screenshot, content_length, all_cookies


class SeleniumChromeBrowserRequest(SeleniumBrowserRequestBase):
    pass


class SeleniumUnitHTMLBrowserRequest(SeleniumBrowserRequestBase):
    pass
