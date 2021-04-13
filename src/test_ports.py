import json
import os

from dotenv import load_dotenv

load_dotenv()


def test_env_ports():
    ports = os.environ.get('PORTS')
    assert type(ports) is str
    assert len(ports) > 0
    json_ports = json.loads(ports)
    assert type(json_ports) is list
