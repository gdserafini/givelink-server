from fastapi.testclient import TestClient
import pytest
from tests.app_test import app


@pytest.fixture
def client():
    return TestClient(app)