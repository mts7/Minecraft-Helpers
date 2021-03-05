import inspect
import json
import os

from dotenv import load_dotenv
from flask import Response

from api import http_codes
from minecraft_helpers.server_actions import MinecraftActions
from mts_utilities import mts_logger

load_dotenv()

DEBUG = os.environ.get('ENVIRONMENT') == 'development'

# set the name of the screen
screen_name = os.environ.get('SCREEN_NAME')

# configure these variables for the Minecraft server
config = {
    'java_executable': os.environ.get('JAVA_EXECUTABLE'),
    'log_level': 'debug' if DEBUG else 'warning',
    'ports': json.loads(os.environ.get('PORTS')),
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
        self.logger = mts_logger.Logger(mode=log_level, log_file='api.log', output='file')

    def check(self):
        """Check if the screen is on or off.

        Returns
        -------
        Response
            The response with the string result and the code.
        """
        result = minecraft_server.screen.check()
        return self.respond('on' if result else 'off')

    def date(self):
        """Get and send the date to the screen session.

        Returns
        -------
        Response
            The response with the string result and the code.
        """
        return self.respond(minecraft_server.send_date())

    def command(self):
        """Get the server command.

        Returns
        -------
        Response
            The response with the string result and the code.
        """
        return self.respond(minecraft_server.get_start_command())

    def create(self):
        """Create the screen session.

        Returns
        -------
        Response
            The response with the string result and the code.
        """
        result = minecraft_server.screen.create()
        if result:
            return self.respond('Created screen', http_codes.NO_CONTENT)
        return self.respond('Failed to create screen', http_codes.SERVICE_UNAVAILABLE)

    def restart(self):
        """Restart the server.

        This returns the combined results from stop and start. While there might be a failed restart value, the server
        might actually be running.

        Returns
        -------
        Response
            The response with the string result and the code.
        """
        result = minecraft_server.restart()
        if result:
            return self.respond('Restarted successfully', http_codes.NO_CONTENT)
        return self.respond('Failed to restart successfully', http_codes.CONFLICT)

    def start(self):
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

    def status(self):
        """Get the status of the server.

        Returns
        -------
        Response
            The response with the string result and the code.
        """
        result = minecraft_server.status()
        return self.respond('up' if result else 'down')

    def stop(self):
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

    def respond(self, message, code=http_codes.OK):
        """Log the request and response and send the response back to the caller.

        Returns
        -------
        Response
            The response with the string result and the code.
        """
        # get the caller method name for logging purposes
        current_frame = inspect.currentframe()
        caller_frame = inspect.getouterframes(current_frame, 2)
        caller = caller_frame[1][3]

        # log the response
        self.logger.info(f'{caller}: Sending API Response, {message}, with code {code}.')

        # return the response with the code
        return Response(message, code)
