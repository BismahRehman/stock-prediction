from fastapi.testclient import TestClient


from app.main import app
# from tests.test_database import TestingAsyncSessionLocal
# from tests.test_dependency import override_get_db

client = TestClient(app)
