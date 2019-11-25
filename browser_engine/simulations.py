"""

"""
import yaml
from extraction_engine import ExtractionEngine
import uuid
import extraction_engine
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class JsonExtractorSimulation:
    """

    simulation = {
           "simulation_id": "step_1",
            "simulation_type": "json_extractor",
            "simulation_code": "- extractor_type: MetaTagExtractor
  extractor_id: meta_tags
- extractor_type: CustomContentExtractor
  extractor_id: content
  data_selectors:
  - selector_id: title
    selector: title
    selector_type: css
    selector_attribute: text
    data_type: RawField"
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
        extraction_manifest = yaml.load(simulation_code, yaml.Loader)
        engine = ExtractionEngine(html=self.browser.page_source(), extraction_manifest=extraction_manifest)
        return engine.extract_data()


class TraversalExtractorSimulation:
    """

    simulation = {
       "simulation_id": "step_1",
        "simulation_type": "traversal_extractor",
        "simulation_code": "- traversal_id: default_traversal
  selector: "a"
  selector_type: css
  selector_attribute: href
  data_type: ListStringField
  max_requests: 500
  next_spider_id: default_spider"
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
        traversal_extraction_manifest = yaml.load(simulation_code, yaml.Loader)
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
        engine = ExtractionEngine(html=self.browser.page_source(), extraction_manifest=traversal_manifests)
        traversal_data_raw = engine.extract_data()

        traversal_data = {}
        if traversal_data_raw is not None:
            for k, v in traversal_data_raw.items():
                traversal_data.update(v)

        return traversal_data


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

    def __init__(self, simulation=None, browser=None, simulation_code_json=None):
        self.simulation = simulation

        # self.simulation_code_json = None
        import time
        time.sleep(1)
        self.browser = browser

    @property
    def simulation_id(self):
        return self.simulation.get("simulation_id")

    def run(self):
        simulation_code = self.simulation.get("simulation_code")
        print("======simulation_code", simulation_code)
        global_fns = {"extraction_engine": extraction_engine}
        # global_fns = {}
        result_data = {
            "data": None,
            "is_simulation_success": False
        }
        exec(simulation_code.strip(), global_fns)
        print("=======d is ", global_fns.keys())
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
        return result_data


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


class WebSimulationManager:

    def __init__(self, simulations=None, request=None, browser=None):
        self.simulations = simulations or {}
        self.request = request
        self.browser = browser

    def run_simulation(self, simulation_id=None, simulation=None):
        logger.debug("Running the simulation for the simulation_id:{}".format(simulation_id))
        print("Running the simulation for the simulation_id:{}".format(simulation_id))
        simulation_type = simulation.get("simulation_type")

        if simulation_type == "json_extractor":
            sim = JsonExtractorSimulation(simulation=simulation, browser=self.browser, )
            return sim.run()
        elif simulation_type == "traversal_extractor":
            sim = JsonExtractorSimulation(simulation=simulation, browser=self.browser)
            return sim.run()
        elif simulation_type == "browser_simulation":
            sim = BrowserSimulation(simulation=simulation, browser=self.browser)
            return sim.run()
        elif simulation_type == "form_submit":
            sim = FormSubmitSimulation(simulation=simulation, browser=self.browser)
            return sim.run()
        elif simulation_type == "get_html":
            return self.browser.page_source()
        elif simulation_type == "get_screenshot":
            return self.browser.get_screenshot()
        else:
            raise NotImplementedError("Simulation with simulation_type={} not implemented!!".format(simulation_type))

    @staticmethod
    def get_elaspsed_time(start_time=None, end_time=None):

        dt = end_time - start_time
        dt_ms = dt.total_seconds() * 1000  # milliseconds
        return "%.2f ms" % dt_ms

    def run(self):
        all_simulations_result = {}
        for simulation_id, simulation in self.simulations.items():
            result = {}
            simulation_start_time = datetime.now()
            try:
                result["result"] = self.run_simulation(
                    simulation_id=simulation_id,
                    simulation=simulation,
                )
                result['error_message'] = None
                result['is_simulation_success'] = True
            except Exception as e:
                result['result'] = None
                result['error_message'] = e.__str__()
                result['is_simulation_success'] = False
            simulation_end_time = datetime.now()
            result['start_time'] = simulation_start_time.__str__()
            result['end_time'] = simulation_end_time.__str__()
            result['elapsed_time_ms'] = self.get_elaspsed_time(start_time=simulation_start_time,
                                                               end_time=simulation_end_time)
            all_simulations_result[simulation_id] = result
        return all_simulations_result
