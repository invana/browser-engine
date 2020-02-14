from .types.extractor import JsonExtractorSimulation, TraversalExtractorSimulation
from .types.simulator import BrowserSimulation
from .types.submitter import FormSubmitSimulation
from datetime import datetime
import logging
from browser_engine.utils import get_elapsed_time

logger = logging.getLogger(__name__)


class WebSimulationManager:

    def __init__(self, simulations=None, request=None, browser=None):
        self.simulations = simulations or {}
        self.request = request
        self.browser = browser

    def run_simulation(self, simulation_id=None, simulation=None):
        logger.debug("Running the simulation for the simulation_id:{}".format(simulation_id), simulation)
        simulation_type = simulation.get("simulation_type")

        if simulation_type == "json_extractor":
            sim = JsonExtractorSimulation(simulation=simulation, browser=self.browser, )
            return sim.run()
        elif simulation_type == "traversal_extractor":
            sim = TraversalExtractorSimulation(simulation=simulation, browser=self.browser)
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

    def run(self):
        all_simulations_result = {}
        job_start_time = datetime.now()

        for simulation_id, simulation in self.simulations.items():
            result = {}
            simulation_start_time = datetime.now()
            try:
                result = self.run_simulation(
                    simulation_id=simulation_id,
                    simulation=simulation,
                )
                result['html'] = self.browser.page_source()
                result['screenshot'] = self.browser.get_screenshot() if self.browser.browser_settings.take_screenshot \
                                                                        is True else None
                result['error_message'] = None
                result['is_simulation_success'] = True
                simulation_end_time = datetime.now()
                result['simulation_start_time'] = simulation_start_time.__str__()
                result['simulation_end_time'] = simulation_end_time.__str__()
                result['simulation_elapsed_time_ms'] = get_elapsed_time(start_time=simulation_start_time,
                                                                        end_time=simulation_end_time)
            except Exception as e:
                result['result'] = None
                result['screenshot'] = None
                result['html'] = None
                result['error_message'] = e.__str__()
                result['is_simulation_success'] = False
                simulation_end_time = datetime.now()
                result['simulation_start_time'] = simulation_start_time.__str__()
                result['simulation_end_time'] = simulation_end_time.__str__()
                result['simulation_elapsed_time_ms'] = get_elapsed_time(start_time=simulation_start_time,
                                                                        end_time=simulation_end_time)

            result['cookies'] = self.browser.driver.get_cookies()
            all_simulations_result[simulation_id] = result
        return all_simulations_result
