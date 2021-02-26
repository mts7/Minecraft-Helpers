#!/usr/local/bin/python3

import subprocess
import sys
import time
from datetime import datetime

import mts_logger


def execute(command: str):
    """Execute the provided command string.

    This executes the command and returns the value sent to stdout.

    Parameters
    ----------
    command : str
        The full string command to execute.

    Returns
    -------
    str
        The result of the process.
    """
    return subprocess.run(command, capture_output=True, check=True, text=True, shell=True).stdout


class ScreenActions:
    logger = None
    name = ''

    def __init__(self, name: str):
        self.name = name
        if self.logger is None:
            self.logger = mts_logger.Logger('info')

    def check(self) -> bool:
        """Check to see if the screen is running.

        This determines if there is at least one screen running with the given
        name.

        Returns
        -------
        bool
            Whether the screen is running or not.
        """
        self.logger.info('check')
        command = 'screen -ls | grep ' + self.name + ' | wc -l'
        self.logger.debug('execute command: ' + command)
        try:
            count = execute(command)
            try:
                return int(count) > 0
            except ValueError as error:
                self.logger.error(str(error))
                return False
        except subprocess.CalledProcessError as error:
            self.logger.error(str(error.returncode) + ': ' + error.stdout)
            return False

    def create(self) -> bool:
        """Start the screen session.

        Start the screen session, regardless of if there is an existing screen
        session with the same name. This is safe and has proper validation.

        This doesn't seem to be working and returns the error, "No screen session
        found."

        Returns
        -------
        bool
            Is the screen on.

        See Also
        --------
        check_screen : The validation necessary for calling this method.
        """
        self.logger.info('create')
        if self.check() is True:
            self.logger.debug('screen is already on')
            return True

        self.logger.debug('starting screen')
        try:
            value = execute('screen -dmS ' + self.name)
            self.logger.debug('value from execute: ' + value)
            self.logger.debug('screen ' + self.name + ' should be running')
            return True
        except subprocess.CalledProcessError as error:
            self.logger.error(str(error.returncode) + ': ' + error.stdout)
            return False

    def send(self, command: str):
        """Send the provided command to the screen.

        This checks for the screen to exist and then directly sends the given
        parameter to the screen using the global variable for screen name. This
        method cannot be called with command line parameters.

        Parameters
        ----------
        command : str
            Command to send to the screen.

        Returns
        -------
        bool|str
            Result of execute or False.
        """
        self.logger.info('send(' + command + ')')
        if self.check() is False:
            self.logger.warning(f'screen {self.name} does not exist.')
            return False

        self.logger.debug('sending command to screen ' + self.name)
        try:
            return execute('screen -dR ' + self.name + ' -X stuff "' + command + '"\015')
        except subprocess.CalledProcessError as error:
            self.logger.error(str(error.returncode) + ': ' + error.stdout)
            return False


class MinecraftActions:
    # configure these variables as necessary
    screen_name = 'm2'
    server_path = '/home/minecraft/minecraft/'
    server_file = 'paper-1.16.5-497.jar'
    stop_timer = 30
    # this should be the path of java on the system
    java_executable = '/usr/bin/java'
    # these are the options for starting the server
    server_options = [
        '-server',
        '-Xms2048M',
        '-Xmx3072M',
        '-XX:+DisableExplicitGC',
        '-XX:+UseAdaptiveGCBoundary',
        '-XX:MaxGCPauseMillis=500',
        '-XX:SurvivorRatio=16',
        '-XX:UseSSE=3',
        '-XX:ParallelGCThreads=2'
    ]
    # do not configure below this line
    starting = False

    def __init__(self):
        # create the logger
        self.logger = mts_logger.Logger('info')

        # get the screen
        self.screen = ScreenActions(self.screen_name)
        self.screen.logger = self.logger

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
        command = self.java_executable + ' ' + ' '.join(
            self.server_options) + ' -jar ' + self.server_path + self.server_file + ' nogui'
        self.logger.debug('command is ' + command)
        return command

    def restart(self):
        """Restart the server by calling stop and then start.

        This is an alias for calling both stop and start. Since both stop and start
        have their own checks, this is safe to call without any other validation.
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

        if self.status():
            self.logger.debug('server is already running')
            return True

        if self.starting:
            self.logger.debug('server is starting')
            return True

        if self.screen.check() is False:
            self.logger.warning('screen is not on')
            return False

        self.starting = True

        self.logger.debug('changing directory to ' + self.server_path)
        result = self.screen.send('cd ' + self.server_path)
        if result is False:
            return False

        command = self.get_start_command()
        result = self.screen.send(command)
        if result is False:
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
        command = 'pidof ' + self.java_executable + ' | wc -l'
        self.logger.debug('execute command: ' + command)
        try:
            count = execute(command)
            self.logger.debug('count from execute is ' + count)
            try:
                return int(count) > 0
            except ValueError as error:
                self.logger.error(str(error))
                return False
        except subprocess.CalledProcessError as error:
            self.logger.error(str(error.returncode) + ': ' + error.stdout)
            return False

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


minecraft_server = MinecraftActions()

# get any command line arguments
if len(sys.argv) > 1:
    action = sys.argv[1]

    # determine which function to call
    switcher = {
        'check': minecraft_server.screen.check,
        'date': minecraft_server.send_date,
        'get': minecraft_server.get_start_command,
        'restart': minecraft_server.restart,
        'screen': minecraft_server.screen.create,
        'start': minecraft_server.start,
        'status': minecraft_server.status,
        'stop': minecraft_server.stop,
        'verify': minecraft_server.verify,
    }

    function_to_call = switcher.get(action, minecraft_server.get_start_command)
    output = function_to_call()
    print(output)
else:
    # display the list of available options
    options = """
Minecraft server-actions.py by Mike Rodarte (mts7777777)
@since 1.16.5

Available Options
================================================================================
check       Check for an existing screen.
date        Send the current date and time to the screen.
get         Print the start server command string to the console.
restart     Stop and start the server.
screen      Create a new screen.
status      Check the server status.
start       Start the server.
stop        Stop the server.
verify      Check to see if the server is running and start if not running.
================================================================================
"""
    print(options)
