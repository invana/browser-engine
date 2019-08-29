import os

AUTH_TOKEN = os.environ.get("AUTH_TOKEN", "iamlazydeveloper")
SELENIUM_HOST = os.environ.get("SELENIUM_HOST", "http://0.0.0.0:4444")

BROWSER_TYPE = os.environ.get("BROWSER_TYPE", "chrome")
BROWSER_SLOTS = os.environ.get("BROWSER_SLOTS", 1)  # used to create n number of browsing instances.
