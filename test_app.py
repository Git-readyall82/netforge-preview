import pytest

import app as app_module


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Use a temporary scores file so tests never touch real scores.
    monkeypatch.setattr(app_module, "SCORES_FILE", tmp_path / "scores.json")
    return app_module.app.test_client()


def all_correct():
    return {str(q["id"]): q["answer"] for q in app_module.QUESTIONS}


def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


def test_questions_do_not_leak_answers(client):
    data = client.get("/api/questions").get_json()
    assert data["count"] == len(app_module.QUESTIONS)
    assert all("answer" not in q for q in data["questions"])


def test_perfect_score(client):
    r = client.post("/api/submit", json={"user": "Anna", "answers": all_correct()})
    assert r.status_code == 200
    assert r.get_json() == {"user": "Anna", "score": 100, "correct": 10, "total": 10}


def test_partial_score(client):
    answers = all_correct()
    for qid in ["1", "2", "3"]:
        answers[qid] = 3  # wrong on purpose
    r = client.post("/api/submit", json={"user": "Ben", "answers": answers})
    assert r.get_json()["score"] == 70


def test_missing_answers_count_as_wrong(client):
    r = client.post("/api/submit", json={"user": "Cara", "answers": {}})
    assert r.get_json()["score"] == 0


def test_missing_user_is_rejected(client):
    r = client.post("/api/submit", json={"user": "", "answers": {}})
    assert r.status_code == 400
    assert "error" in r.get_json()


def test_invalid_json_is_rejected(client):
    r = client.post("/api/submit", data="not json", content_type="text/plain")
    assert r.status_code == 400


def test_scores_are_saved_and_sorted(client):
    client.post("/api/submit", json={"user": "Low", "answers": {}})
    client.post("/api/submit", json={"user": "High", "answers": all_correct()})
    scores = client.get("/api/scores").get_json()["scores"]
    assert [s["user"] for s in scores] == ["High", "Low"]
