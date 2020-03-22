from browser_engine import WebSimulationRequest

url = "https://www.netflix.com/title/70153404?so=su"
default_extraction_manifest = """
- extractor_type: MetaTagExtractor
  extractor_id: meta_tags
"""

click_episodes = """
def simulate(request_object=None):
    print(request_object)
    print(request_object.current_url)
    import time
    time.sleep(4)
    #request_object.implicitly_wait(5)
    print(request_object.page_source)
    request_object.find_element_by_id('tab-Episodes').click()
    time.sleep(4)
    print('Successfully clicked the episodes')
"""
episodes_extraction_manifest = """
- extractor_type: CustomDataExtractor
  extractor_id: episodes
  extractor_fields:
  - field_id: episodes
    element_query:
      type: css
      value: ".episodeLockup"
    data_attribute: element
    data_type: ListDictField
    child_selectors:
    - field_id: title
      element_query:
        value: ".episodeTitle .ellipsized"
      data_attribute: text 
      data_type: StringField
    - field_id: duration
      element_query: 
        value: ".episodeTitle .duration"
      data_attribute: text
      data_type: StringField
    - field_id: duration
      element_query:
        value: ".episodeTitle .duration"
      data_attribute: text
      data_type: StringField
    - field_id: description
      element_query:
        value: ".episodeSynopsis"
      data_attribute: text
      data_type: StringField
    - field_id: url
      element_query:
        value: ".playLink"
      data_attribute: text
      data_type: StringField
    - field_id: image
      element_query:
        value: ".episodeArt"
      data_attribute: src
      data_type: StringField
    
"""
from browser_engine.browsers import SeleniumBrowser, URLLibBrowser

browser = URLLibBrowser(
    headers=None,
    browser_settings={
        "load_images": False,
        "viewport": "1280x720",
        "timeout": 180
    },
)
browser.start_browser()

request = WebSimulationRequest(
    url=url,
    browser=browser,
    tasks={
        "meta_data": {
            "task_type": "json_extractor",
            "task_code": default_extraction_manifest
        },
        "click_episodes": {
            "task_type": "browser_simulation",
            "task_code": click_episodes
        },
        "episodes_data": {
            "task_type": "json_extractor",
            "task_code": episodes_extraction_manifest
        },

    })
response = request.run()

print("=============")
for k, task_result in response['response'].items():
    print(k, task_result)
