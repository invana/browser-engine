from browser_engine import WebSimulationRequest
from browser_engine.browsers.selenium import SeleniumBrowser

browser = SeleniumBrowser(
    headers=None,
    browser_settings={
        "load_images": False,
        "viewport": "1280x720",
        "timeout": 180
    },
)
browser.start()

result = WebSimulationRequest(url="https://invana.io", method="get", browser=browser).run()


print("result", result)