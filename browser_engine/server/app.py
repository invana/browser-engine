from flask import Flask
from flask_restful import Resource, Api
from browser_engine.default_settings import AUTH_TOKEN
from flask import request, render_template
from browser_engine import WebSimulationRequest
from browser_engine.utils import import_klass
import yaml
import os
import logging
from importlib import import_module

logger = logging.getLogger(__name__)
browsers_classes = import_module(f'browser_engine.browsers')

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
templates_folder = os.path.join(BASE_PATH, 'templates')
static_folder = os.path.join(BASE_PATH, 'static')
app = Flask(__name__, static_url_path=static_folder, template_folder=templates_folder)
api = Api(app)


@app.route('/')
def hello():
    token = request.args.get('token')
    if token is None:
        return render_template('homepage.html')
    elif token != AUTH_TOKEN:
        return {"message": "Invalid token, use the token "}, 403
    else:
        context = {"token": token}
        return render_template('simulate.html', **context)


@app.route('/docs.html')
def docs():
    return render_template('docs.html', )


@app.route('/docs/restful-api.html')
def restful_api():
    return render_template('docs/restful-api.html', )


@app.route('/docs/core-concepts.html')
def core_concepts_docs():
    return render_template('docs/core-concepts.html', )


@app.route('/docs/python-api.html')
def python_api():
    return render_template('docs/python-api.html', )


class PingAPIView(Resource):
    def get(self):
        token = request.args.get('token')
        if token != AUTH_TOKEN:
            return {"message": "Invalid token"}, 403
        return {"message": "Bingo! You are authorised to use this service"}


class ExecuteAPIView(Resource):

    @staticmethod
    def create_browser_request(flask_request):
        kwargs = {}
        kwargs['url'] = flask_request.args.get('url')
        kwargs['method'] = flask_request.args.get('http_method', 'get')
        kwargs['debug'] = flask_request.args.get('debug_mode', 0)

        viewport = flask_request.args.get('viewport', default="1280x720")
        load_images = flask_request.args.get('load_images', default=0)
        timeout = int(flask_request.args.get('timeout', default=180))
        browser_settings = {
            "load_images": False if load_images is 0 else True,
            "viewport": viewport,
            "timeout": timeout
        }
        logger.debug("Browser settings is {}".format(browser_settings))
        kwargs['browser_settings'] = browser_settings
        json_data = flask_request.get_json() or {}

        browser_cls = json_data.get("browser_cls")
        kwargs['browser_cls'] = browser_cls
        init_headers = json_data.get("init_headers", None)
        tasks = json_data.get("tasks", {})
        if init_headers:
            if type(init_headers) is not dict:
                init_headers = yaml.load(init_headers, yaml.Loader)
        kwargs['init_headers'] = init_headers
        kwargs['tasks'] = tasks
        return kwargs

    def post(self):
        token = request.args.get('token')
        if token != AUTH_TOKEN:
            return {"message": "Invalid token"}, 403
        kwargs = self.create_browser_request(request)
        browser_cls_path = kwargs['browser_cls'] or "browser_engine.browsers.URLLibBrowser"


        try:
            browser_cls = import_klass(browser_cls_path)
        except AttributeError as e:
            logger.error("Failed to import the browser:{browser_cls_path} with error {error}".format(
                browser_cls_path=browser_cls_path,
                error=e
            ))
            browser_cls = None
        browser = browser_cls(
            headers=kwargs['init_headers'],
            browser_settings=kwargs['browser_settings'],
        )
        browser.start_browser()

        del kwargs['browser_cls']
        del kwargs['browser_settings']
        return WebSimulationRequest(**kwargs, browser=browser).run()


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


# api.add_resource(HelloWorldAPIView, '/')
api.add_resource(PingAPIView, '/ping')
api.add_resource(ExecuteAPIView, '/execute')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
