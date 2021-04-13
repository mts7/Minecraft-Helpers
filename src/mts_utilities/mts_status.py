import subprocess

from .mts_helpers import execute, get_command_path


class StatusChecker:
    """Checks the current status of a process or port."""
    valid = False

    def check(self, command: str):
        """Execute the given command and return a boolean based on the number of
        lines returned from the command.

        Parameters
        ----------
        command : str
            The command to execute (without the `| wc -l`).

        Returns
        -------
        bool|CalledProcessError
            If the number of lines is greater than 0 or an error.
        """
        try:
            count = execute(command + ' | wc -l')
            result = int(count) > 0
            if result:
                self.valid = True
            return result
        except subprocess.CalledProcessError as error:
            return error

    def grep(self, command_name: str) -> bool:
        """Check for a process existing.

        This uses the ps tool with grep to determine if the given command name
        is currently running or not. The command is sent to the check method for
        verification.

        Parameters
        ----------
        command_name : str
            The command/executable name used for searching.

        Returns
        -------
        bool
            Is the executable running.
        """
        return self.check(f'ps aux | grep {command_name} | grep -v grep')

    def port(self, port_numbers: list) -> dict:
        """Checks for listening ports.

        Use netstat to find ports and use grep to find the exact port and if it
        is listening. The command is sent to the check method for verification.

        Parameters
        ----------
        port_numbers : list
            The port numbers to check.

        Returns
        -------
        output : dict
            The dictionary with port number and the result.
        """
        output = {}
        for port_number in port_numbers:
            result = self.check(f'netstat -ane | grep {port_number} | grep LISTEN')
            output['port ' + str(port_number)] = result
        return output

    def process(self, process_name: str, command_name: str):
        """Execute the process name with the command name and check the results.

        The process name should be something that takes a single argument and is
        its own executable file (rather than a command string). This gets the
        full path of the process, then sends a command of that process with the
        command name as a parameter to the check method for verification.

        Parameters
        ----------
        process_name : str
            The name of the executable file that checks for a running process.
        command_name : str
            The name of the command to find by the process.

        Returns
        -------
        bool|CalledProcessError
            The command is currently running or an error.
        """
        try:
            command_path = get_command_path(process_name)
            return self.check(f'{command_path} {command_name}')
        except subprocess.CalledProcessError as error:
            return error
