from browser_engine.default_settings import DEFAULT_SELENIUM_HOST, DEFAULT_BROWSER_TYPE


class DefaultBrowserSettings:
    """

    options = {
        "load_images" : false,
        "enable_adblocker": false,
        "viewport": "1280x720",
        "timeout": 180
    }
    """
    viewport = "1280x720"
    enable_adblocker = False
    load_images = False
    timeout = 180
    browser_type = "CHROME"
    selenium_host = DEFAULT_SELENIUM_HOST

    def __init__(self, options=None):
        if options is not None:
            for k, v in options.items():
                setattr(self, k, v)

    def get_settings(self):
        settings = {}
        for key in self.__dict__.keys():
            settings[key] = getattr(self, key)
        return settings
