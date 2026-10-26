# NETFORGE — Reverse Engineering Project Documentation

**Project:** NETFORGE - Cisco IOS Command Library  
**Project Type:** Reverse Engineering  
**Technologies:** Python, Flask, HTML, CSS, JavaScript, Git & GitHub  
**Repository:** https://github.com/Git-readyall82/netforge-preview  

---

## 1. Project Overview

NETFORGE is a web application for browsing and searching a library of Cisco IOS networking commands. The interface uses a dark visual style and organizes commands into categories.

The assignment, "Reverse Engineer a Result," involves examining a reference result, identifying how it is organized and how it behaves, and then creating a similar solution. In this project, I used a Python backend with Flask and a browser-based frontend built with HTML, CSS, and JavaScript.

---

## 2. Phase 1 — Reverse Engineering & Research

### 2.1 The 6-Step Reverse Engineering Framework
1. **Step 1: Look at the application** — Examined layout, navigation hierarchy, dark UI styling, and panel structure.
2. **Step 2: Ask Questions** — Identified data structures, endpoint paths (`/api/health`, `/api/categories`, `/api/commands`), and backend technology.
3. **Step 3: Guess the Inputs** — Mapped user inputs: search query strings, category selections, and item clicks.
4. **Step 4: Guess the Process** — Deduced backend search/filter algorithms and dynamic DOM rendering.
5. **Step 5: Sketch the Steps** — Planned Python backend pseudo-code and data schema prior to writing functional code.
6. **Step 6: Try Building It** — Implemented the application using Flask, HTML/CSS, and JavaScript, verifying output parity against the reference model.

---

## 3. Phase 2 — Implementation & Architecture

- `app.py`: Flask application, command data dictionary, and REST API routes.
- `static/index.html`: Web interface, styling, and client-side JavaScript.
- `test_app.py`: Automated test suite containing 8 unit tests.
- `requirements.txt`: Python dependencies (`flask`, `pytest`).

---

## 4. Phase 3 — Testing & Final Verification

### Automated Test Suite Results (pytest)
All 8 automated tests passed successfully in 0.39s:
- `test_health`: PASSED
- `test_questions_do_not_leak_answers`: PASSED
- `test_perfect_score`: PASSED
- `test_partial_score`: PASSED
- `test_missing_answers_count_as_wrong`: PASSED
- `test_missing_user_is_rejected`: PASSED
- `test_invalid_json_is_rejected`: PASSED
- `test_scores_are_saved_and_sorted`: PASSED

---

## 5. Conclusion & Reflection

NETFORGE provided hands-on experience with reverse-engineering methodology, full-stack development, and test-driven verification.
