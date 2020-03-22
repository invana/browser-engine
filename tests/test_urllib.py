
from browser_engine.browsers import SeleniumBrowser, URLLibBrowser
from browser_engine import WebSimulationRequest
import pprint


browser = URLLibBrowser(
    headers=None,
    browser_settings={
        "load_images": False,
        "viewport": "1280x720",
        "timeout": 180
    },
)
browser.start_browser()


tasks = {
    "task-1": {
        "task_type": "get_screenshot",
        "task_code": ""
    },
    "task-2": {
        "task_type": "get_html",
        "task_code": ""
    }
}


web_request =  WebSimulationRequest(
                    url= "https://github.com/invanalabs",
                    method="GET",
                    init_headers="",
                    browser=browser,
                    tasks=tasks
                )
response = web_request.run()
pprint.pprint(response)