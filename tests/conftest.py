from copy import deepcopy

import pytest

import src.app as app_module
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def reset_activities():
    original_activities = deepcopy(app_module.activities)
    yield
    app_module.activities = original_activities


@pytest.fixture
def client():
    return TestClient(app_module.app)
