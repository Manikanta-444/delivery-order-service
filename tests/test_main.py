import pytest
import uuid
from fastapi.testclient import  TestClient
from app.main import app
from app.config import UnittestConfig

class TestMain:
    def setup_method(self):
        self.client = TestClient(app)

    def teardown_method(self):
        # Any cleanup can be done here if needed
        pass

    def test_root(self):
        response = self.client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Delivery Order Service is running", "status": "healthy"}

    def test_health_check(self):
        response = self.client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy", "service": "order-service"}