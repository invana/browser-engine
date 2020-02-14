import yaml
from extraction_engine import ExtractionEngine
import uuid
import extraction_engine
import logging

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
