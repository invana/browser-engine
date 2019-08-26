from browser_engine.browsers.splash.default import SplashBrowserRequest
from browser_engine.browsers.selenium.default import SeleniumChromeBrowserRequest
from browser_engine.browsers.core.request import DefaultBrowserRequest
from browser_engine.browsers.core.options import DefaultBrowserOptions


def create_browser_request(flask_request):
    url = flask_request.args.get('url')
    http_method = flask_request.args.get('http_method', 'get')
    browser_type = flask_request.args.get('browser_type', 'default')
    enable_screenshot = flask_request.args.get('enable_screenshot', 0)
    viewport = flask_request.args.get('viewport', "1280x720")
    enable_images = flask_request.args.get('enable_images', 0)
    browser_options = DefaultBrowserOptions(enable_images=enable_images,
                                            enable_screenshot=enable_screenshot,
                                            viewport=viewport)

    if browser_type.lower() == "splash":
        browser_klass = SplashBrowserRequest
    elif browser_type.lower() == "selenium":
        browser_klass = SeleniumChromeBrowserRequest
    else:
        browser_klass = DefaultBrowserRequest

    return browser_klass(url=url, http_method=http_method,
                         browser_type=browser_type,
                         browser_options=browser_options)
