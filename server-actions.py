#!/usr/bin/python

import os
import subprocess
import sys
import time
from datetime import datetime

# configure these variables as necessary
screen_name = 'minecraft'
server_path = '/home/minecraft/minecraft/'
server_file = 'craftbukkit-1.16.5.jar'
stop_timer = 30
# this should be the path of java on the system
java_executable = '/usr/bin/java'
# these are the options for starting the server
server_options = [
    '-server',
    '-Xms2048M',
    '-Xmx5821M',
    '-XX:+UseConcMarkSweepGC',
    '-XX:+UseParNewGC',
    '-XX:+CMSIncrementalPacing',
    '-XX:+UseFastAccessorMethods',
    '-XX:+AggressiveOpts',
    '-XX:+DisableExplicitGC',
    '-XX:+UseAdaptiveGCBoundary',
    '-XX:MaxGCPauseMillis=500',
    '-XX:SurvivorRatio=16',
    '-XX:UseSSE=3',
    '-XX:ParallelGCThreads=2'
]

# DO NOT EDIT THESE VARIABLES
server_starting = False


def check_and_start():
    """Check to see if the server is running and not starting.

    The first check is to see if the server is not running. After that, check
    to see if the server is currently starting. As long as the server is neither
    running nor starting, start the server.
    """
    # be sure to not try to start the server if it's already starting or on
    if not is_server_running() and server_starting is False:
        start_server()


def check_screen():
    """Check to see if the screen is running.

    This uses the global variable, screen_name, to find out how many sessions
    currently exist. If no screen sessions exist with that name, a new screen
    session starts.
    """
    command = 'screen -ls | grep ' + screen_name + ' | wc -l'
    count = execute(command)
    if int(count) == 0:
        start_screen()


def execute(command: str):
    """Execute the provided command string.

    This executes the command and returns the value converted from bytes to string.

    Parameters
    ----------
    command : str
        The full string command to execute.

    Returns
    -------
    result : str
        The bytes, decoded, and turned into a string.
    """
    result = subprocess.run(command, capture_output=True, text=True, shell=True).stdout
    return result


def get_start_command() -> str:
    """Get the Java server command for starting the server.

    This concatenates the Java executable with the server options and the server
    file path and name, providing a full command string for starting the server.

    Returns
    -------
    command: str
        Full executable command to start the Minecraft server.
    """
    command = java_executable + ' ' + ' '.join(server_options) + ' -jar ' + server_path + server_file + ' nogui'
    return command


def is_server_running() -> bool:
    """Check for the Java executable and minecraft in the same process.

    This looks for both the Java executable (from the global variable) and the
    word, minecraft, in a process, and counts the number of lines that exist
    with such conditions. The result is the number of lines being greater than
    zero.

    Returns
    -------
    count: bool
        The result of the comparison of count greater than zero.
    """
    command = 'pidof ' + java_executable + ' | wc -l'
    count = execute(command)
    return int(count) > 0


def restart_server():
    """Restart the server by calling stop and then start.

    This is an alias for calling both stop and start. Since both stop and start
    have their own checks, this is safe to call without any other validation.
    """
    stop_server()
    start_server()


def send_date():
    """Send the current date and time to all logged-in players.

    This gets the current date and time, formats it, and sends it to the screen
    session for all players to see. There is no need to check for the screen
    session since the final function already handles that, making this safe to
    call without validation.
    """
    now = datetime.now()
    formatted = now.strftime("%m/%d/%Y %H:%M:%S")
    send_message('Current time: ' + formatted)


def send_message(message: str):
    """Send a message to the game's chat for all logged-in players to see.

    This takes the message and appends it to the say command, then sends that to
    the screen.

    Parameters
    ----------
    message : str
        Message to display to all users currently in the game.
    """
    send_screen_command('say ' + message)


def send_screen_command(command: str):
    """Send the provided command to the screen.

    This checks for the screen to exist and then directly sends the given
    parameter to the screen using the global variable for screen name.

    Parameters
    ----------
    command : str
        Command to send to the screen.
    """
    check_screen()
    os.system('screen -dR ' + screen_name + ' -X stuff "' + command + '"\015')


def start_screen():
    """Start the screen session.

    Start the screen session, regardless of if there is an existing screen
    session with the same name. This is NOT safe and should only be called
    with proper validation.

    See Also
    --------
    check_screen : The validation necessary for calling this method.
    """
    os.system('screen -dmS ' + screen_name)


def start_server():
    """Start the Minecraft server.

    This checks to see if the server is already running or starting and returns
    if either is true. If the server needs to start, the starting flag changes,
    the screen's directory changes to the server path, and the starting command
    gets pulled and sent to the screen, finally updating the starting flag. This
    has validation and is safe.
    """
    global server_starting
    if is_server_running() or server_starting:
        return
    server_starting = True

    send_screen_command('cd ' + server_path)
    command = get_start_command()
    send_screen_command(command)
    server_starting = False


def stop_server():
    """Stop the Minecraft server.

    This checks to see if the server is already stopped and then continues from
    there. If necessary, this will send a message to the players about a timer,
    trigger the auto-save feature, set a timer, and stop the server. This has
    validation and is safe.
    """
    if not is_server_running() or server_starting:
        return

    send_message('The server is going to be turned off in ' + str(stop_timer) + ' seconds')
    send_screen_command('save-all')
    time.sleep(stop_timer)
    send_screen_command('stop')


# get any command line arguments
if len(sys.argv) > 1:
    action = sys.argv[1]

    # determine which function to call
    switcher = {
        'check': check_and_start,
        'date': send_date,
        'get': get_start_command,
        'restart': restart_server,
        'screen': check_screen,
        'start': start_server,
        'status': is_server_running,
        'stop': stop_server
    }

    function_to_call = switcher.get(action, get_start_command)
    output = function_to_call()
    print(output)
else:
    # display the list of available options
    options = """
    server-actions.py by Mike Rodarte (mts7777777)
    
    Available Options
    ================================================================================
    check       Check to see if the server is running and start if not running.
    date        Send the current date and time to all logged-in players.
    get         Print the start server command string to the console.
    restart     Stop and start the server.
    screen      Check for an existing screen and start one if not open.
    status      Check the server status.
    start       Start the server.
    stop        Stop the server.
    ================================================================================
    """
    print(options)
