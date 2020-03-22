from browser_engine import WebSimulationRequest

url = "https://www.netflix.com/title/70153404?so=su"
default_extraction_manifest = """
- extractor_type: MetaTagExtractor
  extractor_id: meta_tags
"""

click_episodes = """
def simulate(driver=None):
    print(driver)
    print(driver.current_url)
    import time
    time.sleep(4)
    #driver.implicitly_wait(5)
    print(driver.page_source)
    driver.find_element_by_id('tab-Episodes').click()
    time.sleep(4)
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
                               tasks={
                                   "meta_data": {"task_type": "json_extractor",
                                                 "task_code": default_extraction_manifest},
                                   "click_episodes": {"task_type": "browser_simulation",
                                                      "task_code": click_episodes},
                                   "episodes_data": {"task_type": "json_extractor",
                                                     "task_code": episodes_extraction_manifest},

                               })
response = request.run()

print("=============")
for k, task_result in response['response'].items():
    print(k, task_result)
