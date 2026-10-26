# NETFORGE — Network Challenge Arena

NETFORGE is a networking knowledge quiz built with Flask, HTML, CSS and JavaScript. It presents subnetting, VLAN, 802.1Q, OSI and Cisco fundamentals in a dark network-operations interface. The API returns questions without exposing correct answers, calculates submitted scores, and maintains a top-10 leaderboard.

## Features

- Responsive dark interface with electric-blue and gold accents
- Network-map illustration and training-path cards
- Ten multiple-choice networking questions loaded from the API
- Answer progress indicator and score report
- XP-style feedback based on correct answers (display-only; the API stores quiz scores)
- Persistent leaderboard stored in `scores.json`
- Automated API tests

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app run --port 5001
```

Open <http://127.0.0.1:5001> in your browser. Keep the Flask terminal running while you use the page.

## API endpoints

| Method and endpoint | Purpose |
|---|---|
| `GET /api` | API name and endpoint list |
| `GET /api/health` | Health status and question count |
| `GET /api/questions` | Questions and options; correct answers are excluded |
| `POST /api/submit` | Validate a submission, calculate score and save result |
| `GET /api/scores` | Return the top 10 scores |

Example submission body:

```json
{
  "user": "Anna",
  "answers": {"1": 1, "2": 2, "3": 1}
}
```

Answers are option indexes. Questions not answered count as incorrect. The API response contains the user, percentage score, number correct and total number of questions.

## Run tests

```bash
pytest -v
```

The project test suite contains eight tests for health status, answer privacy, perfect and partial scores, missing answers, missing users, invalid JSON, and leaderboard persistence/sorting.

## Reverse-engineering process (APL project)

### Research

The target behavior was described as a quiz API with question retrieval, score submission and a leaderboard. The likely inputs are an operator name and a mapping of question IDs to selected option indexes. The expected outputs are public question data and a score summary.

### Inferred processing logic

1. Keep the correct option index server-side.
2. Return question text and options without the answer key.
3. Accept the user's name and answer mapping as JSON.
4. Compare each submitted option index with the server-side answer.
5. Treat missing answers as incorrect, calculate a percentage, and save the result.
6. Sort saved results by score and return the top ten.

Pseudocode:

```python
def get_score(user_answers):
    correct = 0
    for question in questions:
        if user_answers.get(str(question["id"])) == question["answer"]:
            correct += 1
    total = len(questions)
    return correct, total, round(correct / total * 100)
```

### Implementation and verification

The application uses Flask for HTTP routes and server-side scoring, JSON for API data and saved results, and browser JavaScript to render questions, submit answers and refresh the leaderboard. Run the test suite and manually verify the page in a browser before presenting the final version.

### Problems and solutions log

Record only issues that actually occur during your work. A useful entry includes the observed problem, its cause, the steps used to diagnose it, the fix, and how you verified the fix. One observed frontend issue in the earlier version was that the content appeared very small and shifted to the right in the supplied browser screenshot; the interface has now been redesigned with a responsive centered layout. Add any further issues encountered during browser testing here.

## Presentation checklist

- Explain the goal and reverse-engineering approach in English.
- Show the frontend, one API response, score submission, and leaderboard.
- Run `pytest -v` and show the test results.
- Explain real problems and how they were solved.
- Record a screen-and-audio video of at least four minutes, as required by the course guide.

## Example API checks

```bash
curl http://127.0.0.1:5001/api/questions
curl -X POST http://127.0.0.1:5001/api/submit \
  -H 'Content-Type: application/json' \
  -d '{"user":"Anna","answers":{"1":1,"2":2,"3":1}}'
curl http://127.0.0.1:5001/api/scores
```
