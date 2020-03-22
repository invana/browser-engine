import os

# selenium host will have the browser that is compatible with the the server.
SELENIUM_HOST = os.environ.get("SELENIUM_HOST", "http://127.0.0.1:4444")
BROWSER_TYPE = os.environ.get("BROWSER_TYPE", "selenium-chrome")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN", "iamlazydeveloper")

DEFAULT_BROWSER_TIMEOUT = 120
DEFAULT_USER_AGENT = "https://invana.io/bot.html"
