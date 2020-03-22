from browser_engine import WebSimulationRequest
from browser_engine.browsers import SeleniumBrowser, URLLibBrowser
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

result = WebSimulationRequest(url="https://www.bing.com/", method="get", browser=browser).run()


# print("result", result)
pprint.pprint(result)