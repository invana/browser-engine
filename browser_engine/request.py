"""



"""
from browser_engine.browser import WebBrowser
from datetime import datetime
import socket
from selenium.common.exceptions import TimeoutException
from .simulations import WebSimulationManager


class ClientDetail(object):

    def __init__(self, browser=None):
        self.browser = browser

    def get_elaspsed_time(self):
        if self.browser.started_at:
            dt = datetime.now() - self.browser.started_at
            dt_ms = dt.total_seconds() * 1000  # milliseconds
            return "%.2f ms" % dt_ms
        else:
            return None

    def get_client_details(self):
        return {
            "hostname": socket.gethostname(),
            "ip_address": socket.gethostbyname(socket.gethostname()),
            "browser_type": self.browser.browser_settings.browser_type,
            "elasped_time_ms": self.get_elaspsed_time()
        }


class WebSimulationRequest:
    started_at = datetime.now()

    def __init__(self, url=None,
                 method="GET",
                 headers=None,
                 browser_settings=None,
                 simulations=None):
        if headers:
            headers = {k.lower(): v for k, v in headers.items()}
        if method:
            method = method.upper()
        self.url = url
        self.method = method
        self.headers = headers
        self.simulations = simulations or []
        self.browser = WebBrowser(url=url, method=method, headers=headers, browser_settings=browser_settings,
                                  request=self)
        self.browser.start()
        print("Browser started ")
        self.simulation_manager = WebSimulationManager(request=self, browser=self.browser, simulations=simulations)

    def run(self):

        message = {
            "message": "Ok",
            "client": ClientDetail(browser=self.browser).get_client_details(),
            "request": {
                "url": self.url,
                "method": self.method,
                "headers": self.headers,
                "browser_settings": self.browser.browser_settings.get_settings()
            },
        }
        try:
            message["response"] = self.simulation_manager.run()
        except Exception as e:
            message["response"] = {
                "__error_message": e.__str__()
            }
        self.browser.close_browser()

        return message
