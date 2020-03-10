import requests
from urllib.parse import quote_plus

payload = {"init_headers": "", "tasks": {"task-1": {"task_type": "get_screenshot", "task_code": ""}}}
response = requests.post("http://0.0.0.0:5000/execute?url={url}&viewport=1280x720&timeout=180&method=get"
                         "&load_images=0&token=iamlazydeveloper".format(
    url=quote_plus("http://invana.io")),
    data=payload)
print(response.status_code)
print(response.json())
