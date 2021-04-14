import os
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, Response

import src.api.handler as handler
from src.api import http_codes

load_dotenv()

app = Flask(__name__)

DEBUG = os.environ.get('ENVIRONMENT') == 'development'
app.config['DEBUG'] = DEBUG
api_handler = handler.ApiHandler('debug' if DEBUG else 'info')


def authenticate_user(callback: callable):
    """Authenticate the user.

    Parameters
    ----------
    callback : callable
        Function to handle the successful authentication of the user.

    Returns
    -------
    callable | Response
    """

    @wraps(callback)
    def wrapper(*args, **kwargs):
        # TODO: add actual authentication with JWT or similar
        auth = DEBUG
        if not auth:
            api_handler.logger.error('Unauthorized user')
            return Response('Not Authenticated', http_codes.UNAUTHORIZED,
                            {'WWW-Authenticate': 'Bearer realm="Token"'})
        return callback(*args, **kwargs)

    return wrapper


def authenticate_admin(callback: callable):
    """Authenticate an administrator.

    Parameters
    ----------
    callback : callable

    Returns
    -------
    callable | Response
    """

    @wraps(callback)
    def wrapper(*args, **kwargs):
        # TODO: add actual authentication with JWT or similar
        auth = DEBUG
        if not auth:
            api_handler.logger.error('Unauthorized admin')
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
def page_not_found(error) -> Response:
    """Display a generic error page for all errors.

    Parameters
    ----------
    error

    Returns
    -------
    Response
    """

    api_handler.logger.error(str(error))
    return Response('What is it you are trying to find?', http_codes.NOT_FOUND)


@app.route('/api/check', methods=['GET'])
@authenticate_user
def check():
    """Call the check method of the API handler.

    Returns
    -------
    Response
    """
    return api_handler.check()


@app.route('/api/date', methods=['POST'])
@authenticate_user
def date():
    """Call the date method of the API handler.

    Returns
    -------
    Response
    """
    return api_handler.date()


@app.route('/api/command', methods=['GET'])
@authenticate_admin
def command():
    """Call the command method of the API handler.

    Returns
    -------
    Response
    """
    return api_handler.command()


@app.route('/api/restart', methods=['PUT', 'PATCH'])
@authenticate_user
def restart():
    """Call the restart method of the API handler.

    Returns
    -------
    Response
    """
    return api_handler.restart()


@app.route('/api/create', methods=['POST'])
@authenticate_admin
def create():
    """Call the create method of the API handler.

    Returns
    -------
    Response
    """
    return api_handler.create()


@app.route('/api/start', methods=['POST'])
@authenticate_user
def start():
    """Call the start method of the API handler.

    Returns
    -------
    Response
    """
    return api_handler.start()


@app.route('/api/status', methods=['GET'])
def status():
    """Call the status method of the API handler.

    Returns
    -------
    Response
    """
    return api_handler.status()


@app.route('/api/stop', methods=['DELETE'])
@authenticate_user
def stop():
    """Call the stop method of the API handler.

    Returns
    -------
    Response
    """
    return api_handler.stop()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
