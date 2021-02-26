import subprocess


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
    result = subprocess.run(command, capture_output=True, check=True, text=True, shell=True).stdout
    return result.strip()


def get_command_path(command_name: str):
    """Gets the full path of the executable identified by the command_name.

    This only works on operating systems that have the `which` command.

    Parameters
    ----------
    command_name : str
        The command name to lookup on Linux

    Returns
    -------
    bool|str
        Full path of the executable or False on failure.
    """
    return execute(f'which {command_name}')
