import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import app as application

def setup_function():
    application.tasks[:] = [
        {"id": 1, "title": "Understand CI/CD pipeline", "done": False},
        {"id": 2, "title": "Build Docker image", "done": True},
    ]
    application.next_id = 3

def test_home_page_loads():
    response = application.app.test_client().get("/")
    assert response.status_code == 200
    assert b"Student Task Manager" in response.data

def test_health_endpoint():
    response = application.app.test_client().get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "ok"

def test_add_task():
    client = application.app.test_client()
    response = client.post("/add", data={"title": "Deploy to Minikube"})
    assert response.status_code == 302
    assert any(t["title"] == "Deploy to Minikube" for t in application.tasks)

def test_toggle_task():
    application.app.test_client().post("/toggle/1")
    assert application.tasks[0]["done"] is True
