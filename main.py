import sys

import minecraft_helpers.give as give
from minecraft_helpers.server_actions import MinecraftActions

# set the name of the screen
screen_name = 'm2'

# start the giver
giver = give.Give(screen_name)

# configure these variables for the Minecraft server
config = {
    'java_executable': 'java',
    'ports': [25565, 8123],
    'screen_name': screen_name,
    'server_path': '/home/minecraft/minecraft/',
    'server_file': 'paper-1.16.5-497.jar',
    'stop_timer': 30,
    'server_options': [
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
}
minecraft_server = MinecraftActions(**config)


def display_menu():
    # display the list of available options
    options = """
Minecraft server_actions.py by Mike Rodarte (mts7777777)
@since 1.16.5

Available Options
================================================================================
check       Check for an existing screen.
date        Send the current date and time to the screen.
get         Print the start server command string to the console.
give        Give an item with enchantments through a menu system.
restart     Stop and start the server.
screen      Create a new screen.
status      Check the server status.
start       Start the server.
stop        Stop the server.
verify      Check to see if the server is running and start if not running.
================================================================================
"""
    print(options)


def handle_action(action: str):
    # determine which function to call
    switcher = {
        'check': minecraft_server.screen.check,
        'date': minecraft_server.send_date,
        'get': minecraft_server.get_start_command,
        'give': giver.prompt_categories,
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


if __name__ == '__main__':
    # get any command line arguments
    if len(sys.argv) > 1:
        handle_action(sys.argv[1])
    else:
        display_menu()
