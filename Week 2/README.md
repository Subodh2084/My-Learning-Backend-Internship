# Week 2: FastAPI & Starlette — REST Mini Project

This repository houses the core deliverables for **Week 2 of the Backend Development Internship**. The objective this week was to construct a structurally decoupled, fully tested RESTful API using [FastAPI](https://tiangolo.com) and [Starlette](https://starlette.io), focusing on isolating the transport layer (HTTP handling/schema validation) from the core business logic (service layer) to keep the engine ready for a future GraphQL migration.

---


## 📊 Week 2 Sprint & Deliverables Tracker

| Day | Module / Concept | Task / Objective | Status | Artifact / Deliverable | Verified Checkpoint |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **Day 06** | **FastAPI Request Lifecycle** | Implement `main.py` routing, run Uvicorn, and trace an active request model. |      Complete | `app/main.py`<br> | • `/health` and `/tasks` return valid JSON.<br>• Uvicorn starts via CLI.<br>• Docs visible at `/docs`. |
| **Day 07** | **Schemas & Status Codes** | Build explicit typed input/output Pydantic schemas and catch validation edge cases. |      Complete | `app/schemas/tasks.py`<br>↳ Validation Contract Logs | • Title string constraints enforced.<br>• Malformed inputs caught as `422 Unprocessable Entity`. |
| **Day 08** | **CRUD & Service Boundaries**| Separate transport logic from service layer. Handle stable IDs and deletions. |      COmplete | `app/services/tasks.py`<br>↳ CRUD Router Set | • Read-after-delete fails cleanly.<br>• 404 handled for missing IDs.<br>• Persistence limit documented. |
| **Day 09** | **Starlette Middleware & Errors** | Inject request tracing IDs, duration logging, and fire-and-forget background metrics. |      Complete | `app/middleware/`<br>↳ Application Error Format | • `X-Request-ID` logs generated.<br>• Credentials stripped from trace logs.<br>• Background task durability note added. |
| **Day 10** | **REST Mini Project Review** | Consolidate code base, run 5+ target integration tests via HTTPX, and perform peer clone test. | ⬜ | `tests/test_tasks.py`<br>↳ Complete Test Report | • 5+ meaningful criteria assertions validated.<br>• Robust assertions (No blind `200 OK` reliance). |

---

