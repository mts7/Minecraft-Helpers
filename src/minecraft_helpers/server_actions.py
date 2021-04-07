import subprocess
import time
from datetime import datetime

import mtslogger
from mts_utilities.mts_helpers import get_command_path
from mts_utilities.mts_screen import ScreenActions
from mts_utilities.mts_status import StatusChecker


class MinecraftActions:
    # do not configure below this line
    starting = False

    def __init__(self, screen_name='minecraft', log_level='info',
                 server_path='/usr/games/minecraft',
                 server_file='minecraft_server.jar', stop_timer=30,
                 java_executable='/bin/java', server_options=None, ports=None):
        if ports is None:
            ports = []
        if server_options is None:
            server_options = []
        # create the logger
        self.logger = mtslogger.get_logger(__name__, mode=log_level)

        # set the instance properties from the keyword arguments
        self.ports = ports if len(ports) > 0 else [25565]
        self.server_options = server_options
        self.server_path = server_path
        self.server_file = server_file
        self.stop_timer = stop_timer
        self.java_executable = java_executable

        # get the screen
        self.screen = ScreenActions(name=screen_name, logger=self.logger)

        # get the status checker
        self.status_checker = StatusChecker()
        self.status_checker.logger = self.logger

    def get_date(self) -> str:
        """Get the current date in a readable format.

        This method cannot be called with command line parameters.

        Returns
        -------
        str
            The date formatted like 12/31/2020 23:59:59.
        """
        self.logger.info('get_date')
        now = datetime.now()
        return now.strftime("%m/%d/%Y %H:%M:%S")

    def get_start_command(self) -> str:
        """Get the Java server command for starting the server.

        This concatenates the Java executable with the server options and the server
        file path and name, providing a full command string for starting the server.

        Returns
        -------
        command: str
            Full executable command to start the Minecraft server.
        """
        self.logger.info('get_start_command')

        try:
            path_java = get_command_path(self.java_executable)
        except subprocess.CalledProcessError as error:
            self.logger.error(str(error.returncode) + ': ' + error.stdout)
            return ''

        command = path_java + ' ' + ' '.join(
            self.server_options) + ' -jar ' + self.server_path + self.server_file + ' nogui'
        self.logger.debug('command is ' + command)
        return command

    def restart(self) -> bool:
        """Restart the server by calling stop and then start.

        This is an alias for calling both stop and start. Since both stop and start
        have their own checks, this is safe to call without any other validation.

        Returns
        -------
        bool
            Stopped and started results
        """
        self.logger.info('restart')
        stopped = self.stop()
        if stopped:
            self.logger.debug('waiting to give status a chance to catch up')
            time.sleep(5)
            started = self.start()
            if started is False:
                self.logger.warning('failed to start the server')
            else:
                self.logger.debug('done restarting')
        else:
            self.logger.warning('failed to stop the server')
            started = False
        return stopped and started

    def send_date(self):
        """Send the current date and time to all logged-in players.

        This gets the current date and time, formats it, and sends it to the screen
        session for all players to see. There is no need to check for the screen
        session since the final function already handles that, making this safe to
        call without validation.
        """
        self.logger.info('send_date')
        message = 'Current time: ' + self.get_date()
        self.logger.debug(message)
        self.send_message(message)

    def send_message(self, message: str):
        """Send a message to the game's chat for all logged-in players to see.

        This takes the message and appends it to the say command, then sends
        that to the screen. This method cannot be called with a command line
        parameter.

        Parameters
        ----------
        message : str
            Message to display to all users currently in the game.
        """
        self.logger.info('send_message(' + message + ')')
        result = self.screen.send('say ' + message)
        if result is not False:
            self.logger.debug('done sending screen command')

    def start(self) -> bool:
        """Start the Minecraft server.

        This checks to see if the server is already running or starting and
        returns if either is true. If the server needs to start, the starting
        flag changes, the screen's directory changes to the server path, and the
        starting command gets pulled and sent to the screen, finally updating
        the starting flag. This has validation and is safe.

        Returns
        -------
        bool
            Did the server start successfully.
        """
        self.logger.info('start')

        if self.screen.check() is False:
            self.logger.warning('screen is not on')
            return False

        if self.status():
            self.logger.debug('server is already running')
            return True

        if self.starting:
            self.logger.debug('server is starting')
            return True

        self.starting = True

        self.logger.debug('changing directory to ' + self.server_path)
        result = self.screen.send('cd ' + self.server_path)
        if result is False:
            self.starting = False
            return False

        command = self.get_start_command()
        if command == '':
            self.starting = False
            return False

        result = self.screen.send(command)
        if result is False:
            self.starting = False
            return False

        # TODO: poll the screen to determine if the server is done
        self.logger.debug('waiting for server to load...')
        # wait for the server and world to load
        time.sleep(30)

        self.starting = False
        self.logger.debug('done starting server')

        return True

    def status(self) -> bool:
        """Check for the PID of the executable.

        This looks for the PID of the executable and counts the number of lines
        that exist with such conditions. The result is the number of lines being
        greater than zero.

        Returns
        -------
        bool
            The result of the comparison of count greater than zero.
        """
        self.logger.info('status')

        # reset valid before checking
        self.status_checker.valid = False

        # get the status from the status checker
        status = {
            'pidof': self.status_checker.process('pidof', self.java_executable),
            'pgrep': self.status_checker.process('pgrep', self.java_executable),
            **(self.status_checker.port(self.ports)),
            'ps': self.status_checker.grep(self.java_executable)
        }
        # this is only for logging/debugging purposes
        if self.logger.mode == 'debug':
            for key in status:
                self.logger.debug(f'{key} status is {status[key]}')

        # if any of them are True, valid will be True
        return self.status_checker.valid

    def stop(self) -> bool:
        """Stop the Minecraft server.

        This checks to see if the server is already stopped and then continues from
        there. If necessary, this will send a message to the players about a timer,
        trigger the auto-save feature, set a timer, and stop the server. This has
        validation and is safe.

        Returns
        -------
        bool
            Did the stop command finish successfully.
        """
        self.logger.info('stop')

        if self.status() is False:
            self.logger.warning('server is not running, so it cannot be stopped')
            return False

        if self.starting:
            self.logger.warning('server is starting and cannot be stopped')
            return False

        self.send_message('The server is going to be turned off in ' + str(self.stop_timer) + ' seconds')
        result = self.screen.send('save-all')
        if result is False:
            return False

        self.logger.debug('waiting for ' + str(self.stop_timer) + ' seconds to give users time to exit')
        time.sleep(self.stop_timer)

        result = self.screen.send('stop')
        if result is False:
            return False

        self.logger.debug('done stopping server')

        return True

    def verify(self) -> bool:
        """Check to see if the server is running and not starting.

        The first check is to see if the server is not running. After that, check
        to see if the server is currently starting. As long as the server is neither
        running nor starting, start the server.

        Returns
        -------
        bool
            Is the server running.
        """
        self.logger.info('verify')

        if self.screen.check() is False:
            self.logger.warning('screen is not on')
            return False

        # be sure to not try to start the server if it's already starting or on
        if self.status() is True:
            self.logger.debug('server is running')
            return True

        if self.starting is True:
            self.logger.debug('server is starting')
            return True

        # the server should be running, so getting to this point is unexpected
        self.logger.warning('server is not running or starting')

        return self.start()
