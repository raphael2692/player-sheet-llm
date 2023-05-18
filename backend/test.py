# run with pytest test.py

from common import set_env, LOGGER
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_read_main():
    response = client.get("/test_with_fake_prompt_and_sheet")
    assert response.status_code == 200