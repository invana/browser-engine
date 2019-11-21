from flask import Flask
from flask_restful import Resource, Api
from browser_engine.default_settings import AUTH_TOKEN
from flask import request, render_template
from browser_engine import WebSimulationRequest
import yaml
import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
templates_folder = os.path.join(BASE_PATH, 'templates')
static_folder = os.path.join(BASE_PATH, 'static')
app = Flask(__name__, static_url_path=static_folder, template_folder=templates_folder)
api = Api(app)


@app.route('/')
def hello():
    token = request.args.get('token')
    return render_template('homepage.html')


@app.route('/render.html')
def render():
    token = request.args.get('token')
    if token != AUTH_TOKEN:
        return {"message": "Invalid token"}, 403
    context = {"token": token}
    return render_template('render.html', **context)


@app.route('/docs.html')
def docs():
    return render_template('docs.html', )


@app.route('/extract.html')
def extract():
    token = request.args.get('token')
    if token != AUTH_TOKEN:
        return {"message": "Invalid token"}, 403
    context = {"token": token}
    return render_template('extract.html', **context)


@app.route('/simulate.html')
def simulate():
    token = request.args.get('token')
    if token != AUTH_TOKEN:
        return {"message": "Invalid token"}, 403
    context = {"token": token}
    return render_template('simulate.html', **context)


@app.route('/form.html')
def form():
    token = request.args.get('token')
    if token != AUTH_TOKEN:
        return {"message": "Invalid token"}, 403
    context = {"token": token}
    return render_template('form.html', **context)


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

        take_screenshot = int(flask_request.args.get('take_screenshot', 0))
        viewport = flask_request.args.get('viewport', "1280x720")
        enable_images = flask_request.args.get('enable_images', 0)
        timeout = int(flask_request.args.get('timeout', 180))
        browser_type = flask_request.args.get('browser_type', "chrome")

        browser_settings = {
            "enable_images": False if enable_images is 0 else True,
            "take_screenshot": False if take_screenshot is 0 else True,
            "viewport": viewport,
            "timeout": timeout,
            "browser_type": browser_type
        }
        kwargs['browser_settings'] = browser_settings
        json_data = flask_request.get_json() or {}
        headers = json_data.get("headers", None)
        simulations = json_data.get("simulations", {})

        if headers:
            if type(headers) is not dict:
                headers = yaml.load(headers, yaml.Loader)
        kwargs['headers'] = headers
        kwargs['simulations'] = simulations
        return kwargs

    def post(self):
        token = request.args.get('token')
        if token != AUTH_TOKEN:
            return {"message": "Invalid token"}, 403
        kwargs = self.create_browser_request(request)

        return WebSimulationRequest(**kwargs).run()


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


# api.add_resource(HelloWorldAPIView, '/')
api.add_resource(PingAPIView, '/ping')
api.add_resource(ExecuteAPIView, '/execute')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
