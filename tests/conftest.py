import pytest
import json
from importlib import resources
from . import example_files

@pytest.fixture
def json_example():
    return resources.read_text(example_files, "ex1.json")