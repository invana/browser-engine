import yaml
from extraction_engine import ExtractionEngine
import uuid
import extraction_engine
import logging
logger = logging.getLogger(__name__)


class BrowserSimulation:
    """

    simulation = {
           "simulation_id": "step_1",
            "simulation_type": "browser_simulation",
            "simulation_code": "def simulate(driver=None):
    import random
    driver.switch_to.default_content()
    driver.implicitly_wait(random.randint(0, 2))
    print ('Successfully waited for sometime')"
    }

    """

    def __init__(self, simulation=None, browser=None):
        self.simulation = simulation

        # self.simulation_code_json = None
        import time
        time.sleep(1)
        self.browser = browser

    @property
    def simulation_id(self):
        print("simulation_od", self.simulation)
        return self.simulation.get("simulation_id")

    def run(self):
        simulation_code = self.simulation.get("simulation_code")
        global_fns = {"extraction_engine": extraction_engine}
        # global_fns = {}
        result_data = {
            "data": None,
            "simulation_type": self.simulation.get("simulation_type"),
            "is_simulation_success": False
        }
        exec(simulation_code.strip(), global_fns)
        simulate_fn = global_fns['simulate']
        driver = self.browser.driver
        # setattr(driver, "simulation_code", simulation_code)

        if simulate_fn:
            try:
                data = simulate_fn(driver=driver)
                result_data['data'] = data
                result_data['is_simulation_success'] = True
            except Exception as e:
                print("Simulation failed with error", e)
                result_data['error_message'] = str(e)
        return result_data
