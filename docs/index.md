# Browser Engine


Here is the notes on advanced implementation.




## Setup Selenium Server (optional) 

### method 1 - standalone setup
```bash
wget https://selenium-release.storage.googleapis.com/3.141/selenium-server-standalone-3.141.59.jar
java -jar selenium-server-standalone-3.141.59.jar # starts selenium webdriver at http://0.0.0.0:4444
```


### method2 - via docker 
```bash
docker run --name selenium-cr -d -p 4444:4444 -v /dev/shm:/dev/shm selenium/standalone-chrome:3.141.59-titanium
docker run --name selenium-ff -d -p 4445:4444 -v /dev/shm:/dev/shm selenium/standalone-firefox:3.141.59-vanadium
# or use ` --shm-size 2g ` instead of `-v /dev/shm:/dev/shm` depending on what best suits for you.
```

## Setup RESTful server (optional)

### method1 - running as  
```bash
# setup environment variables needed
export SELENIUM_HOST=http://0.0.0.0:4444 # selenium host
export AUTH_TOKEN=iamlazydeveloper
export BROWSER_TYE=selenium-chrome

# starting the server 
uwsgi --socket 0.0.0.0:5000 --protocol=http -w browser_engine.server.wsgi:application --processes 4 --threads 2
```

## Setup Selenium

```bash

# 2. Deploying a browser engine container
git clone git@github.com:invanalabs/browser-engine.git
docker build -t browser-engine --build-arg selenium_host="http://xxx.xx.xx.xx:4444"  \
 --build-arg auth_token="iamlazydeveloper" --build-arg browser_type="selenium-chrome" -f Dockerfile .
docker run  --name browser-engine -d -p 5000:5000 browser-engine 
```