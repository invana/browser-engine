from flask import Flask
from flask_restful import Resource, Api
from browser_engine.browsers.core.response import DefaultBrowserResponse
from browser_engine.browsers.default import create_browser_request
from browser_engine.settings import AUTH_TOKEN
from flask import request

app = Flask(__name__)
api = Api(app)


class HelloWorldAPIView(Resource):
    def get(self):
        token = request.args.get('token')
        if token != AUTH_TOKEN:
            return {"message": "Invalid token"}, 403
        browser_request = create_browser_request(request)
        return DefaultBrowserResponse(request=browser_request,
                                      message="Hello World. Welcome to Browser Engine").get_response()


class PingAPIView(Resource):
    def get(self):
        token = request.args.get('token')
        if token != AUTH_TOKEN:
            return {"message": "Invalid token"}, 403
        return DefaultBrowserResponse().get_response()


class RenderAPIView(Resource):
    def get(self):
        token = request.args.get('token')
        if token != AUTH_TOKEN:
            return {"message": "Invalid token"}, 403
        browser_request = create_browser_request(request)
        return DefaultBrowserResponse(request=browser_request, message="Alright! Rendered the url").get_response()


api.add_resource(HelloWorldAPIView, '/')
api.add_resource(PingAPIView, '/ping')
api.add_resource(RenderAPIView, '/render')

if __name__ == '__main__':
    app.run(debug=True)
