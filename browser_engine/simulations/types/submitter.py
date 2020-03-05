import yaml
import logging

logger = logging.getLogger(__name__)


class FormSubmitSimulation:
    """

    task = {
           "task_id": "step_1",
            "task_type": "form_submit",
            "task_code": "def simulate(driver=None):
    import random
    driver.switch_to.default_content()
    driver.implicitly_wait(random.randint(0, 2))
    print ('Successfully waited for sometime')"
    }

    """

    def __init__(self, task=None, browser=None):
        self.task = task
        self.browser = browser

    @property
    def task_id(self):
        return self.task.get("task_id")

    def run(self):
        task_code = self.task.get("task_code")
        form_manifest = yaml.load(task_code, yaml.Loader)

        form_selector = form_manifest.get("form_identifier")
        if form_selector:
            form_element = self.browser.get_element(selector=form_selector)
        else:
            form_element = None
        for selector in form_manifest['fields']:
            el = self.browser.get_element(selector=selector,
                                          parent_element=form_element if form_element else self.browser)
            if el:
                el.send_keys(selector['field_value'])

        submit_element = self.browser.get_element(selector=form_manifest['submit_identifier'],
                                                  parent_element=form_element if form_element else self.browser)
        if submit_element:
            submit_element.click()
        return None
