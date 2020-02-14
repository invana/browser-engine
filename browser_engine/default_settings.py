import os

# selenium host will have the browser that is compatible with the the server.
SELENIUM_HOST = os.environ.get("SELENIUM_HOST", "http://localhost:4444")
BROWSER_TYPE = os.environ.get("BROWSER_TYPE", "CHROME")

AUTH_TOKEN = os.environ.get("AUTH_TOKEN", "iamlazydeveloper")
