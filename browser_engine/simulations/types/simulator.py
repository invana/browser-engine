import yaml
from extraction_engine import ExtractionEngine
import uuid
import extraction_engine
import logging
logger = logging.getLogger(__name__)


class BrowserSimulation:
    """

    simulation = {
           "task_id": "step_1",
            "task_type": "browser_simulation",
            "task_code": "def simulate(driver=None):
    import random
    driver.switch_to.default_content()
    driver.implicitly_wait(random.randint(0, 2))
    print ('Successfully waited for sometime')"
    }

    """

    def __init__(self, task=None, browser=None):
        self.task = task

        # self.task_code_json = None
        import time
        time.sleep(1) # TODO - check and remove why we need this.
        self.browser = browser

    @property
    def task_id(self):
        return self.task.get("task_id")

    def run(self):
        task_code = self.task.get("task_code")
        global_fns = {"extraction_engine": extraction_engine}
        # global_fns = {}
        result_data = {
            "data": None,
            "task_type": self.task.get("task_type"),
            "is_task_success": False
        }
        exec(task_code.strip(), global_fns)
        simulate_fn = global_fns['simulate']
        driver = self.browser.driver
        # setattr(driver, "task_code", task_code)

        if simulate_fn:
            try:
                data = simulate_fn(driver=driver)
                result_data['data'] = data
                result_data['is_task_success'] = True
            except Exception as e:
                print("task failed with error", e)
                result_data['error_message'] = str(e)
        return result_data
