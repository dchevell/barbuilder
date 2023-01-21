import pytest

import os

script ='/path/to/script.py'

os.environ['SWIFTBAR_PLUGIN_PATH'] = script

@pytest.fixture
def script_path():
    return script

