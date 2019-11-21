from browser_engine import WebSimulationRequest

url = "https://www.netflix.com/title/81011159"
default_extraction_manifest = """
- extractor_type: MetaTagExtractor
  extractor_id: meta_tags
"""

click_episodes = """
def simulate(driver=None):
    driver.find_element_by_id('tab-Episodes').click()
    driver.implicitly_wait(3)
    print('Successfully clicked the episodes')
"""
episodes_extraction_manifest = """
- extractor_type: CustomContentExtractor
  extractor_id: episodes
  data_selectors:
  - selector_id: episodes
    selector: ".episodeLockup"
    selector_type: css
    selector_attribute: element
    data_type: ListDictField
    child_selectors:
    - selector_id: title
      selector: ".episodeTitle .ellipsized"
      selector_type: css
      selector_attribute: text
      data_type: StringField
    - selector_id: duration
      selector: ".episodeTitle .duration"
      selector_type: css
      selector_attribute: text
      data_type: StringField
    - selector_id: duration
      selector: ".episodeTitle .duration"
      selector_type: css
      selector_attribute: text
      data_type: StringField
    - selector_id: description
      selector: ".episodeSynopsis"
      selector_type: css
      selector_attribute: text
      data_type: StringField
    - selector_id: url
      selector: ".playLink"
      selector_type: css
      selector_attribute: text
      data_type: StringField
    - selector_id: image
      selector: ".episodeArt"
      selector_type: css
      selector_attribute: src
      data_type: StringField
    
"""

request = WebSimulationRequest(url=url,
                               # browser_settings={"selenium_host": "http://192.168.0.10:4444"},
                               simulations={
                                   "meta_data": {"simulation_type": "json_extractor",
                                                 "simulation_code": default_extraction_manifest},
                                   "click_episodes": {"simulation_type": "browser_simulation",
                                                      "simulation_code": click_episodes},
                                   "episodes_data": {"simulation_type": "json_extractor",
                                                     "simulation_code": episodes_extraction_manifest},

                               })
response = request.run()

print(response)
print(response.keys())
print(response['response'].keys())

for k, simulation in response['response'].items():
    print(k, simulation['error_message'])
    print(k, simulation['result'])
