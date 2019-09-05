from flask import Flask
from flask_restful import Resource, Api
from browser_engine.browsers.core.response import DefaultBrowserResponse
from browser_engine.browsers.default import create_browser_request
from browser_engine.settings import AUTH_TOKEN
from flask import request, render_template

app = Flask(__name__, static_url_path="/static")
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


class PingAPIView(Resource):
    def get(self):
        token = request.args.get('token')
        if token != AUTH_TOKEN:
            return {"message": "Invalid token"}, 403
        return DefaultBrowserResponse().get_response()


class RenderAPIView(Resource):

    def post(self):
        token = request.args.get('token')
        if token != AUTH_TOKEN:
            return {"message": "Invalid token"}, 403
        browser_request = create_browser_request(request)
        return DefaultBrowserResponse(request=browser_request, message="Alright! Rendered the url").get_response()


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


# api.add_resource(HelloWorldAPIView, '/')
api.add_resource(PingAPIView, '/ping')
api.add_resource(RenderAPIView, '/render')

if __name__ == '__main__':
    app.run(debug=True)
