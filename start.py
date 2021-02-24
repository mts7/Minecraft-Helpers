#!/usr/bin/python
import os
import subprocess
import sys

# this should be the path of java on the system
java_executable = '/usr/bin/java'
# configure these variables as necessary
server_path = '/home/minecraft/minecraft/'
server_file = 'craftbukkit-1.16.5.jar'
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
# this is the beginning of the no-edit zone
base_command = java_executable + ' '


def get_start_command():
    command = base_command + ' '.join(server_options) + ' -jar ' + server_path + server_file + ' nogui'
    return command


def is_server_running():
    count = subprocess.check_output('ps aux | grep ' + java_executable + ' | grep minecraft | wc -l', shell=True)
    return count > 0


def start_server():
    if is_server_running():
        return

    command = get_start_command()
    os.system(command)


# get any command line arguments
if len(sys.argv) > 1:
    action = sys.argv[1]
else:
    action = 'get'

switcher = {
    'check': is_server_running,
    'get': get_start_command,
    'start': start_server
}

function_to_call = switcher.get(action, get_start_command)
output = function_to_call()
print(output)
