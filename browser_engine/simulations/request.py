from datetime import datetime
from browser_engine.utils import convert_yaml_to_json
from browser_engine.simulations.manager import WebSimulationManager
from browser_engine.utils import get_elapsed_time
import socket


class ClientDetail(object):

    def __init__(self, browser=None):
        self.browser = browser

    def get_elapsed_time(self):
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
            "elapsed_time_ms": self.get_elapsed_time()
        }


class RequestPayloadValidator:
    pass


class WebSimulationRequest:
    started_at = datetime.now()

    def __init__(self, url=None,
                 method="GET",
                 init_headers=None,
                 browser=None,
                 tasks=None,
                 debug=None,):
        """


        :param url:
        :param method:
        :param init_headers: can be dict
        :param tasks:
        """

        if isinstance(init_headers, str):
            init_headers = convert_yaml_to_json(init_headers)
        if init_headers:
            init_headers = {k.lower(): v for k, v in init_headers.items()}
        if method:
            method = method.upper()
        self.url = url
        self.method = method
        self.init_headers = init_headers
        self.tasks = tasks or []
        self.debug = debug
        self.browser = browser
        self.task_manager = WebSimulationManager(request=self, browser=self.browser, tasks=tasks, debug=debug)

    def run(self):
        request_start_time = datetime.now()
        print("self.url",self.url)
        self.browser.load_page(url=self.url)

        message = {
            "message": "Ok",
            "client": ClientDetail(browser=self.browser).get_client_details(),
            "request": {
                "url": self.url,
                "method": self.method,
                "init_headers": self.init_headers,
                "browser_settings": self.browser.browser_settings.get_settings(),
                "tasks": self.tasks
            },
            "response": {}
        }
        try:
            message["response"]['task_results'] = self.task_manager.run()
        except Exception as e:
            message["response"] = {
                "task_results": None,
                "__error_message": e.__str__()
            }
        request_end_time = datetime.now()
        message['response']['client'] = {
            'job_start_time': request_start_time.__str__(),
            'job_end_time': request_end_time.__str__(),
            'job_elapsed_time_ms': get_elapsed_time(start_time=request_start_time,
                                                    end_time=request_end_time)
        }

        self.browser.stop_browser()
        return message
