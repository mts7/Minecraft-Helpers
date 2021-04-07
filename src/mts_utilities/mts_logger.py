import sys
from datetime import datetime

from colorama import init, Back, Fore, Style

init()


class Logger:
    """Encapsulate the logging methods.

    This is the standard logger for use with this package. It is in its basic
    stage, but it is functional. The basic usage is
    ```
    import mts_logger
    logger = mts_logger.Logger('info')
    logger.warning('What is going on here?')
    ```
    """

    # these are the variables that are better off left alone
    message_colors = {
        'error': Fore.RED,
        'warning': Fore.LIGHTYELLOW_EX,
        'info': Fore.LIGHTCYAN_EX,
        'debug': Back.LIGHTYELLOW_EX + Fore.BLACK
    }
    modes = ['error', 'warning', 'info', 'debug']
    outputs = {
        'error': sys.stderr,
        'file': 'file',
        'out': sys.stdout
    }

    def __init__(self, mode='warning', output='out', log_file='', use_error=True):
        """Initialize the object with the desired mode.

        Mode can be any of the values as seen in the `modes` variable.

        Parameters
        ----------
        mode : str
            The default value is warning so that error and warning are displayed.
        log_file : str
            The file path and name to use for writing.
        output : str
            The output method (as indexed in outputs).
        use_error : bool
            Whether the messages should go to stderr or stdout when out is the output value.
        """
        if mode in self.modes:
            self.mode = mode
        else:
            self.mode = 'warning'

        if log_file != '':
            self.log_file = log_file

        self.output = output
        self.use_error = use_error

    def log(self, message: str):
        """Log a message with the current log level.

        This method can be used to log an entry no matter the mode because it
        logs using the current mode.

        Parameters
        ----------
        message : str
            The message to log.
        """
        switcher = {
            'debug': self.debug,
            'error': self.error,
            'info': self.info,
            'warning': self.warning
        }

        function_to_call = switcher.get(self.mode, self.info)
        # noinspection PyArgumentList
        function_to_call(message)

    def debug(self, message: str):
        """Log the message at the debug log level.

        Parameters
        ----------
        message : str
            The message to log.
        """
        self.write('debug', message)

    def error(self, message: str):
        """Log the message at the error log level.

        Parameters
        ----------
        message : str
            The message to log.
        """
        self.write('error', message)

    def info(self, message: str):
        """Log the message at the info log level.

        Parameters
        ----------
        message : str
            The message to log.
        """
        self.write('info', message)

    def warning(self, message: str):
        """Log the message at the warning log level.

        Parameters
        ----------
        message : str
            The message to log.
        """
        self.write('warning', message)

    def write(self, level: str, message: str):
        """Write the actual message using the given log level.

        This checks the position of the log level and the current mode and
        writes the log if and only if the log level is less than or equal to the
        current mode level. From there, it determines if the error should be
        written to stdout or stderr. After that, it checks for a file and writes
        the message to the desired output.

        Parameters
        ----------
        level : str
            The log level for writing. This determines the color and might
            determine the output.
        message : str
            The message to log.
        """
        mode_position = self.modes.index(self.mode)
        log_position = self.modes.index(level)
        if log_position <= mode_position:
            if level == 'error' and self.output == 'out' and self.use_error:
                # switch to stderr when output is out and use error is true
                output = self.outputs['error']
            else:
                if self.output not in self.outputs:
                    # in case output is incorrect, set to the default
                    self.output = 'out'
                output = self.outputs[self.output]

            date = datetime.now().isoformat(' ', 'seconds')
            if output == 'file':
                with open(self.log_file, 'a') as fileObject:
                    prefix = f'{date} {level}: '
                    print(prefix + message, file=fileObject)
            else:
                print(date + ' ' + self.message_colors[level] + message + Style.RESET_ALL, file=output)
