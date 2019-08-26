# Browser Grid


## Install

```bash
pip install -e git+https://github.com/crawlerflow/browser-engine.git#egg=browser_engine
```


## Setup

```bash

export BROWSER_TYPE=selenium
export BROWSER_HOST=http://0.0.0.0:4444 # selenium path
export AUTH_TOKEN=iamlazydeveloper

```


## To Start the Server 

```bash
uwsgi --socket 0.0.0.0:5000 --protocol=http -w browser_engine.server.wsgi:application

or 

python -m browser_engine.server.app
```




## How to make a call

```bash
curl -XGET http://localhost:5000/render?url=http://invanalabs.ai&browser_type=selenium&token=iamlazydeveloper
```

