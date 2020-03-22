import os

# selenium host will have the browser that is compatible with the the server.
DEFAULT_SELENIUM_HOST = os.environ.get("DEFAULT_SELENIUM_HOST", "http://127.0.0.1:4444")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN", "iamlazydeveloper")

DEFAULT_USER_AGENT = "https://invana.io/bot.html"

DEFAULT_BROWSER = "browser_engine.browsers.URLLibBrowser"
DEFAULT_BROWSER_TYPE = os.environ.get("DEFAULT_BROWSER_TYPE", "selenium-chrome")
DEFAULT_BROWSER_TIMEOUT = 120
