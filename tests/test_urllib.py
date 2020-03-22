from browser_engine.browsers import URLLibBrowser

browser = URLLibBrowser()
browser.request(url="https://invana.io", method="get")
page = browser.read()
print(page)
