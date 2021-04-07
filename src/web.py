import os
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, Response

import api.handler as handler
from api import http_codes

load_dotenv()

app = Flask(__name__)

DEBUG = os.environ.get('ENVIRONMENT') == 'development'
app.config['DEBUG'] = DEBUG
apiHandler = handler.ApiHandler('debug' if DEBUG else 'info')


def authenticate_user(callback):
    @wraps(callback)
    def wrapper(*args, **kwargs):
        # TODO: add actual authentication with JWT or similar
        auth = DEBUG
        if not auth:
            apiHandler.logger.error('Unauthorized user')
            return Response('Not Authenticated', http_codes.UNAUTHORIZED, {'WWW-Authenticate': 'Bearer realm="Token"'})
        return callback(*args, **kwargs)

    return wrapper


def authenticate_admin(callback):
    @wraps(callback)
    def wrapper(*args, **kwargs):
        # TODO: add actual authentication with JWT or similar
        auth = DEBUG
        if not auth:
            apiHandler.logger.error('Unauthorized admin')
            return Response('Forbidden', http_codes.FORBIDDEN)
        return callback(*args, **kwargs)

    return wrapper


@app.errorhandler(http_codes.BAD_REQUEST)
@app.errorhandler(http_codes.UNAUTHORIZED)
@app.errorhandler(http_codes.FORBIDDEN)
@app.errorhandler(http_codes.NOT_FOUND)
@app.errorhandler(http_codes.METHOD_NOT_ALLOWED)
@app.errorhandler(http_codes.INTERNAL_SERVER_ERROR)
@app.errorhandler(http_codes.BAD_GATEWAY)
@app.errorhandler(http_codes.SERVICE_UNAVAILABLE)
@app.errorhandler(http_codes.GATEWAY_TIMEOUT)
def page_not_found(error):
    apiHandler.logger.error(str(error))
    return Response('What is it you are trying to find?', http_codes.NOT_FOUND)


@app.route('/api/check', methods=['GET'])
@authenticate_user
def check():
    return apiHandler.check()


@app.route('/api/date', methods=['POST'])
@authenticate_user
def date():
    return apiHandler.date()


@app.route('/api/command', methods=['GET'])
@authenticate_admin
def command():
    return apiHandler.command()


@app.route('/api/restart', methods=['PUT', 'PATCH'])
@authenticate_user
def restart():
    return apiHandler.restart()


@app.route('/api/create', methods=['POST'])
@authenticate_admin
def create():
    return apiHandler.create()


@app.route('/api/start', methods=['POST'])
@authenticate_user
def start():
    return apiHandler.start()


@app.route('/api/status', methods=['GET'])
def status():
    return apiHandler.status()


@app.route('/api/stop', methods=['DELETE'])
@authenticate_user
def stop():
    return apiHandler.stop()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
