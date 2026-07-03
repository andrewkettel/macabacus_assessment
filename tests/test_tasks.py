from uuid import uuid4

import pytest

from ..models.task import StatusEnum, Task
from ..routers.tasks import tasks


@pytest.fixture(autouse=True)
def reset_tasks_db():
    yield
    tasks.clear()


def add_task(title: str, status: StatusEnum):
    task = Task(title=title, status=status)
    tasks.append(task)
    return task


def test_get_tasks(test_client):
    add_task("Complete the project", StatusEnum.ToDo)

    response = test_client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Complete the project"
    assert response.json()[0]["status"] == "todo"


def test_get_tasks_filtered(test_client):
    add_task("Start the project", StatusEnum.Done)
    add_task("Complete the project", StatusEnum.ToDo)

    response = test_client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 2

    response = test_client.get("/tasks?status=todo")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Complete the project"
    assert response.json()[0]["status"] == "todo"

    response = test_client.get("/tasks?status=done")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Start the project"
    assert response.json()[0]["status"] == "done"


def test_create_task(test_client):
    response = test_client.post(
        "/tasks", json={"title": "Complete the project", "status": "todo"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Complete the project"
    assert response.json()["status"] == "todo"


def test_update_task(test_client):
    task = add_task("Complete the project", StatusEnum.ToDo)

    response = test_client.patch(
        f"/tasks/{str(task.id)}",
        json={"title": "Complete the project", "status": "in_progress"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Complete the project"
    assert response.json()["status"] == "in_progress"


def test_update_task_not_found(test_client):
    add_task("Complete the project", StatusEnum.ToDo)

    uuid = uuid4()
    response = test_client.patch(
        f"/tasks/{uuid}",
        json={"title": "Complete the project", "status": "in_progress"},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == f"Task with id {uuid} not found"


def test_create_task_unique_id(test_client):
    task = add_task("Complete the project", StatusEnum.ToDo)

    response = test_client.post(
        "/tasks",
        json={"id": str(task.id), "title": "Complete the project", "status": "todo"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Task id is not unique"
