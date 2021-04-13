import json
import os

from dotenv import load_dotenv

load_dotenv()

# get ports from environment
ports = os.environ.get('PORTS')
assert isinstance(ports, str)
ports_length = len(ports)
assert ports_length > 0
json_ports = json.loads(ports)
if isinstance(json_ports, str):
    json_ports = json.loads(json_ports)
assert isinstance(json_ports, list)

# configure these variables for the Minecraft server
config = {
    'java_executable': os.environ.get('JAVA_EXECUTABLE'),
    'log_level': 'debug' if os.environ.get('ENVIRONMENT') == 'development' else 'warning',
    'ports': json.loads(os.environ.get('PORTS')),
    'screen_name': os.environ.get('SCREEN_NAME'),
    'server_file': os.environ.get('SERVER_FILE'),
    'server_path': os.environ.get('SERVER_PATH'),
    'stop_timer': os.environ.get('STOP_TIMER'),
    'server_options': json.loads(os.environ.get('SERVER_OPTIONS'))
}
