import pytest
import json
from importlib import resources
from . import example_files

@pytest.fixture
def json_example1():
    return resources.read_text(example_files, "ex1.json")

@pytest.fixture
def json_example2():
    return resources.read_text(example_files, "ex2.json")
    
@pytest.fixture
def json_example3():
    return resources.read_text(example_files, "ex3.json")