class BrowserOptionsBase(object):

    def __init__(self,
                 enable_images=False,
                 take_screenshot=False,
                 enable_adblocker=False,
                 viewport="1024x768"

                 ):
        self.enable_images = enable_images
        self.enable_adblocker = enable_adblocker
        self.take_screenshot = False if take_screenshot is 0 else True
        self.viewport = viewport

        # self.browser_height = viewport.split("x")[1]
        # self.browser_width = viewport.split("x")[0]

    def get_options(self):
        return {
            "enable_images": self.enable_images,
            "enable_adblocker": self.enable_adblocker,
            "take_screenshot": self.take_screenshot,
            "viewport": self.viewport,
            # "browser_height": self.browser_height,
            # "browser_width": self.browser_width
        }


class DefaultBrowserOptions(BrowserOptionsBase):
    pass
