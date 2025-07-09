from fastapi.testclient import TestClient
from uv_starter.api.main import app

client = TestClient(app)


class TestAPI:
    def test_root_endpoint(self):
        response = client.post(
            "/",
            json={"num_1": 40, "num_2": 2},
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 200
        assert response.json() == {"message": "the sum is 42"}
