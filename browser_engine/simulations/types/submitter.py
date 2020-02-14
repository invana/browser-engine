import yaml
import logging

logger = logging.getLogger(__name__)


class FormSubmitSimulation:
    """

    simulation = {
           "simulation_id": "step_1",
            "simulation_type": "form_submit",
            "simulation_code": "def simulate(driver=None):
    import random
    driver.switch_to.default_content()
    driver.implicitly_wait(random.randint(0, 2))
    print ('Successfully waited for sometime')"
    }

    """

    def __init__(self, simulation=None, browser=None):
        self.simulation = simulation
        self.browser = browser

    @property
    def simulation_id(self):
        return self.simulation.get("simulation_id")

    def run(self):
        simulation_code = self.simulation.get("simulation_code")
        form_manifest = yaml.load(simulation_code, yaml.Loader)

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
