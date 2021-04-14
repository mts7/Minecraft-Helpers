import subprocess

import mtslogger

from .mts_helpers import execute

log_level = 'info'


class ScreenActions:
    """All actions that integrate with `screen`."""

    name = ''

    def __init__(self, name: str, logger=None):
        self.name = name
        if logger is None:
            self.logger = mtslogger.get_logger(__name__, mode=log_level)
        else:
            self.logger = logger

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
        self.logger.debug(f'execute command: {command}')
        try:
            count = execute(command)
            try:
                return int(count) > 0
            except ValueError as error:
                self.logger.error(str(error))
                return False
        except subprocess.CalledProcessError as error:
            self.logger.error(f'{str(error.returncode)}: {error.stdout}')
            return False

    def create(self) -> bool:
        """Start the screen session.

        Start the screen session, regardless of if there is an existing screen
        session with the same name. This is safe and has proper validation.

        This doesn't seem to be working and returns the error, "No screen
        session found."

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
            value = execute(f'screen -dmS {self.name}')
            self.logger.debug(f'value from execute: {value}')
            self.logger.debug(f'screen {self.name} should be running')
            return True
        except subprocess.CalledProcessError as error:
            self.logger.error(f'{str(error.returncode)}: {error.stdout}')
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
        self.logger.info(f'send({command})')
        if self.check() is False:
            self.logger.warning(f'screen {self.name} does not exist.')
            return False

        self.logger.debug(f'sending command to screen {self.name}')
        try:
            return execute(
                'screen -dR ' + self.name + ' -X stuff "' + command + '"\015'
            )
        except subprocess.CalledProcessError as error:
            self.logger.error(f'{str(error.returncode)}: {error.stdout}')
            return False
