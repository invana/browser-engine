class BrowserOptionsBase(object):

    def __init__(self,
                 enable_images=False,
                 enable_screenshot=False,
                 enable_adblocker=False,
                 viewport="1024x768"

                 ):
        self.enable_images = enable_images
        self.enable_adblocker = enable_adblocker
        self.enable_screenshot = enable_screenshot
        self.viewport = viewport
        # self.browser_height = viewport.split("x")[1]
        # self.browser_width = viewport.split("x")[0]

    def get_options(self):
        return {
            "enable_images": self.enable_images,
            "enable_adblocker": self.enable_adblocker,
            "enable_screenshot": self.enable_screenshot,
            "viewport": self.viewport,
            # "browser_height": self.browser_height,
            # "browser_width": self.browser_width
        }


class DefaultBrowserOptions(BrowserOptionsBase):
    pass
