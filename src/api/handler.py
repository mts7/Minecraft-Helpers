import inspect
import json
import os

import mtslogger
from dotenv import load_dotenv
from flask import Response, request

from src.api import http_codes
from src.minecraft_helpers.server_actions import MinecraftActions

load_dotenv()

DEBUG = os.environ.get('ENVIRONMENT') == 'development'

# set the name of the screen
screen_name = os.environ.get('SCREEN_NAME')

# handle ports early
ports = os.environ.get('PORTS')
assert type(ports) is str
ports_length = len(ports)
print(f'ports length: {ports_length}')
assert ports_length > 0
print(f'ports: {ports}')
json_ports = json.loads(ports)
print('json: ', json_ports)
assert type(json_ports) is list

# configure these variables for the Minecraft server
config = {
    'java_executable': os.environ.get('JAVA_EXECUTABLE'),
    'log_level': 'debug' if DEBUG else 'warning',
    'ports': json_ports,
    'screen_name': screen_name,
    'server_file': os.environ.get('SERVER_FILE'),
    'server_path': os.environ.get('SERVER_PATH'),
    'stop_timer': os.environ.get('STOP_TIMER'),
    'server_options': json.loads(os.environ.get('SERVER_OPTIONS'))
}
minecraft_server = MinecraftActions(**config)


class ApiHandler:
    def __init__(self, log_level='info'):
        # create the logger
        self.logger = mtslogger.get_logger(__name__, mode=log_level,
                                           log_file='api.log', output='file')

    def check(self) -> Response:
        """Check if the screen is on or off.

        Returns
        -------
        Response
            The response with the string result and the code.
        """
        result = minecraft_server.screen.check()
        return self.respond('on' if result else 'off')

    def date(self) -> Response:
        """Get and send the date to the screen session.

        Returns
        -------
        Response
            The response with the string result and the code.
        """
        return self.respond(minecraft_server.send_date())

    def command(self) -> Response:
        """Get the server command.

        Returns
        -------
        Response
            The response with the string result and the code.
        """
        return self.respond(minecraft_server.get_start_command())

    def create(self) -> Response:
        """Create the screen session.

        Returns
        -------
        Response
            The response with the string result and the code.
        """
        result = minecraft_server.screen.create()
        if result:
            return self.respond('Created screen', http_codes.NO_CONTENT)
        return self.respond('Failed to create screen',
                            http_codes.SERVICE_UNAVAILABLE)

    def restart(self) -> Response:
        """Restart the server.

        This returns the combined results from stop and start. While there might
        be a failed restart value, the server might actually be running.

        Returns
        -------
        Response
            The response with the string result and the code.
        """
        result = minecraft_server.restart()
        if result:
            return self.respond('Restarted successfully', http_codes.NO_CONTENT)
        return self.respond('Failed to restart successfully',
                            http_codes.CONFLICT)

    def start(self) -> Response:
        """Start the server.

        Returns
        -------
        Response
            The response with the string result and the code.
        """
        result = minecraft_server.start()
        if result:
            return self.respond('Started successfully', http_codes.NO_CONTENT)
        return self.respond('Failed to start', http_codes.CONFLICT)

    def status(self) -> Response:
        """Get the status of the server.

        Returns
        -------
        Response
            The response with the string result and the code.
        """
        result = minecraft_server.status()
        return self.respond('up' if result else 'down')

    def stop(self) -> Response:
        """Stop the server.

        Returns
        -------
        Response
            The response with the string result and the code.
        """
        result = minecraft_server.stop()
        if result:
            return self.respond('Stopped successfully', http_codes.NO_CONTENT)
        return self.respond('Failed to stop', http_codes.CONFLICT)

    def respond(self, message, code=http_codes.OK) -> Response:
        """Log the request and response and send the response back to the
        caller.

        Returns
        -------
        Response
            The response with the string result and the code.
        """
        # get the caller method name for logging purposes
        current_frame = inspect.currentframe()
        caller_frame = inspect.getouterframes(current_frame, 2)
        caller = caller_frame[1][3]

        # get the IP address
        other = request.headers.getlist('X-Forwarded-For')
        if len(other) > 0:
            ip = ', '.join(other)
        else:
            ip = request.remote_addr

        # log the response
        self.logger.info(f'{ip} - {caller}: Sending API Response, {message}, '
                         f'with code {code}.')

        # return the response with the code
        return Response(message, code)
