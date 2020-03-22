from .types.extractor import JsonExtractorSimulation, TraversalExtractorSimulation,\
    HTMLExtractor, ScreenshotExtractor
from .types.simulator import BrowserSimulation
from .types.submitter import FormSubmitSimulation
from datetime import datetime
import logging
from browser_engine.utils import get_elapsed_time

logger = logging.getLogger(__name__)


class WebSimulationManager:

    def __init__(self, tasks=None, request=None, browser=None, debug=None):
        self.tasks = tasks or {}
        self.request = request
        self.browser = browser
        self.debug = debug

    def run_simulation(self, task_id=None, task=None):
        logger.debug("Running the task for the task_id:{} with payload {}".format(task_id, task))
        task_type = task.get("task_type")
        if task_type == "json_extractor":
            sim = JsonExtractorSimulation(task=task, browser=self.browser)
            return sim.run()
        elif task_type == "traversal_extractor":
            sim = TraversalExtractorSimulation(task=task, browser=self.browser)
            return sim.run()
        elif task_type == "browser_simulation":
            sim = BrowserSimulation(task=task, browser=self.browser)
            return sim.run()
        elif task_type == "form_submit":
            sim = FormSubmitSimulation(task=task, browser=self.browser)
            return sim.run()
        elif task_type == "get_html":
            return HTMLExtractor(task=task, browser=self.browser).run()
        elif task_type == "get_screenshot":
            return ScreenshotExtractor(task=task, browser=self.browser).run()
        else:
            raise NotImplementedError("task with task_type={} not implemented!!".format(task_type))

    def run(self):
        all_simulations_result = {}

        for task_id, task in self.tasks.items():
            result = {}
            task_start_time = datetime.now()
            try:
                result = self.run_simulation(
                    task_id=task_id,
                    task=task,
                )
                if self.debug == 1:
                    result['html'] = self.request.browser.page_source()
                    result['screenshot'] = self.request.browser.get_screenshot() if \
                        self.browser.browser_settings.take_screenshot \
                        is True else None
                result['error_message'] = None
                result['is_task_success'] = True
                task_end_time = datetime.now()
                result['task_start_time'] = task_start_time.__str__()
                result['task_end_time'] = task_end_time.__str__()
                result['task_elapsed_time_ms'] = get_elapsed_time(start_time=task_start_time,
                                                                  end_time=task_end_time)
            except Exception as e:
                result['result'] = None
                if self.debug == 1:
                    result['screenshot'] = None
                    result['html'] = None
                result['error_message'] = e.__str__()
                result['is_task_success'] = False
                task_end_time = datetime.now()
                result['task_start_time'] = task_start_time.__str__()
                result['task_end_time'] = task_end_time.__str__()
                result['task_elapsed_time_ms'] = get_elapsed_time(start_time=task_start_time,
                                                                  end_time=task_end_time)

            result['cookies'] = self.request.browser.driver.get_cookies()
            all_simulations_result[task_id] = result
        return all_simulations_result
