# Browser Grid

Library to integrate browsers like selenium, splash with CrawlerFlow 

## Install

```bash
pip install -e git+https://github.com/crawlerflow/browser-engine.git#egg=browser_engine
```


## Setup

```bash

export BROWSER_TYPE=selenium
export SELENIUM_HOST=http://0.0.0.0:4444 # selenium host
export AUTH_TOKEN=iamlazydeveloper

```
Currently BROWSER_TYPE can be `selenium` or `splash`. 

With BROWSER_TYPE=splash, SELENIUM_HOST would be http://0.0.0.0:8050 or relevant.

## To Start the Server 

```bash
uwsgi --socket 0.0.0.0:5000 --protocol=http -w browser_engine.server.wsgi:application --processes 4 --threads 2

or 

python -m browser_engine.server.app
```




## How to make a call

```bash
curl -XGET http://localhost:5000/render?url=http://github.com/login&browser_type=selenium&token=iamlazydeveloper
```

```json

{
	"url" :"http://github.com/login",
	"script": null,
	"browser_settings": {
		"viewport": "1280x720",
		"loading_options": {
			"load_images": false,
			"load_scripts": false,
			"load_stylesheets": false
		}
	},
	"cookies": null,
	"headers": null,
	"take_screenshot": false,
	"tasks": []

}
```

