# 40-Day Advanced Backend Engineering Curriculum

Welcome to the **40-Day Backend Engineering Internship**. This repository tracks the progression from Python and architectural foundations to production-ready deployment, caching, and regression testing. Each week focuses on a core backend pillar, culminating in a concrete, verifiable deliverable.

---

##  Curriculum Overview

| Week | Focus | Core Tools | Weekly Deliverable | Status |
| :--- | :--- | :--- | :--- | :---: |
| **1** | Python & Project Foundation | Python, Git, Venv, IDE/Editor | Typed validation/service exercises & clean Git history |   [ Ongoing Day 2 Complete] |
| **2** | FastAPI & Starlette | FastAPI, Uvicorn, Pydantic, HTTPX, Pytest | Tested REST mini-project with meaningful errors & logs |   [ ] |
| **3** | PostgreSQL & Schema History | PostgreSQL, SQLAlchemy, Alembic, SQL Client | Persistent task data, migrations, & activity tracking |   [ ] |
| **4** | Authentication & Authorization | pwdlib (Argon2), PyJWT, Pytest | Verified sessions, multi-user ownership checks |   [ ] |
| **5** | GraphQL with Ariadne | Ariadne, GraphQL Schema | REST/GraphQL rule consistency & bounded queries |   [ ] |
| **6** | Failure Handling & Caching | Redis, ARQ, Core Failure Fixtures | Resilient core behavior with scoped cache/worker labs |   [ ] |
| **7** | Docker Compose & Readiness | Docker, Compose, Service DNS, Healthchecks | Multi-container stack with self-healing DB dependencies |   [ ] |
| **8** | Regression & Handover | Pytest, Ruff, Mypy, CI Config | Fully linted backend, regression evidence, & runbook |   [ ] |

---

##  Weekly Breakdowns & Deliverables

### Week 1: Python & Project Foundation (Days 1–5)
* **Focus:** Establishing environment isolation, strict type safety, and professional version control workflows.
* **Tools:** Python 3.11+, Git, `venv`/`poetry`, VS Code/Cursor/PyCharm.
* **Deliverable:** A fresh project repository containing typed validation exercises, isolated service patterns, and a highly readable, atomic Git history.

### Week 2: FastAPI & Starlette (Days 6–10)
* **Focus:** Building robust asynchronous RESTful APIs, structured request validation, and comprehensive API integration testing.
* **Tools:** FastAPI, Uvicorn, Pydantic v2, HTTPX, Pytest.
* **Deliverable:** A tested REST mini-project featuring production-grade global exception handlers and structured JSON logging.

### Week 3: PostgreSQL Persistence & Schema History (Days 11–15)
* **Focus:** Relational database modeling, asynchronous ORM configuration, and programmatic database migration tracking.
* **Tools:** PostgreSQL, SQLAlchemy (Async), Alembic, DBeaver/pgAdmin.
* **Deliverable:** A persistent data layer featuring task management tables, an automated activity/audit log, and a clean history of reviewed Alembic migrations.

### Week 4: Authentication & Authorization (Days 16–20)
* **Focus:** Implementing secure password hashing, stateless token management, and strict resource-level access control.
* **Tools:** `pwdlib` (Argon2), PyJWT, Pytest.
* **Deliverable:** An auth system validating user sessions, multi-user resource ownership checks, and secure public-facing Pydantic schemas that filter out sensitive data.

### Week 5: GraphQL with Ariadne (Days 21–25)
* **Focus:** Exposing a schema-first GraphQL API alongside existing REST endpoints while ensuring business logic parity.
* **Tools:** Ariadne, GraphQL Core.
* **Deliverable:** A functional GraphQL gateway maintaining authorization consistency with the REST layer, featuring bounded queries to prevent deep nesting exploits.

### Week 6: Failure Handling with Cache & Job Labs (Days 26–30)
* **Focus:** Introducing system resilience, circuit breakers, caching strategies, and offloading heavy tasks to asynchronous workers.
* **Tools:** Redis, ARQ, Custom Failure Fixtures.
* **Deliverable:** A resilient backend architecture containing scoped cache-aside experiments and background worker execution logs.

### Week 7: Docker Compose & Readiness (Days 31–35)
* **Focus:** Containerizing applications, managing multi-service networking, and implementing deterministic service startup order.
* **Tools:** Docker, Docker Compose, Service DNS, Healthchecks.
* **Deliverable:** A complete application stack that spins up seamlessly, persists data across container restarts, and gracefully recovers if the database dependency fails during startup.

### Week 8: Regression & Handover (Days 36–40)
* **Focus:** Code quality enforcement, static analysis, continuous integration setup, and project finalization.
* **Tools:** Pytest, Ruff, Mypy, GitHub Actions / GitLab CI.
* **Deliverable:** A fully reviewed backend with 100% pass rates on type-checking and testing pipelines, complete with a reproducible operational runbook.

---


