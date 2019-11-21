import os

SELENIUM_HOST = os.environ.get("SELENIUM_HOST", "http://localhost:4444")
BROWSER_TYPE = os.environ.get("BROWSER_TYPE", "chrome")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN", "iamlazydeveloper")
