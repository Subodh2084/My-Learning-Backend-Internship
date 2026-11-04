# 🗓️ Week 3 Progress: PostgreSQL Persistence & Schema History

## 🎯 Weekly Objectives & Tools
* **Core Concepts:** Data persistence, primary/foreign key relationships, atomic transactions, schema migrations, and request-scoped session lifecycles.
* **Stack:** PostgreSQL, SQLAlchemy (ORM), Alembic (Migrations), SQL Client, MongoDB (Extra Practice).
* **Weekly Output:** Persistent private task data, reviewed migration versions, and a relational activity/audit history table.

---

## 📋 Daily Schedule & Deliverables Tracking

| Day | Focus / Concept | Onsite Steps & Milestones | Acceptance Criteria | Deliverables / Status |
| :--- | :--- | :--- | :--- | :--- |
| **Day 11** | **PostgreSQL Setup & Schema** | <ul><li>[ Completed] Spin up PostgreSQL lab container</li><li>[ Completed] Design Users, Projects, Tasks schema</li><li>[ Completed] Write synthetic data insertion script</li></ul> | Connection is reproducible; primary/foreign keys strictly enforce relational integrity. | <ul><li>[ Completed] Schema diagram</li><li>[ Completed] SQL seed examples</li><li>[ Completed] Connection notes</li></ul> |
| **Day 12** | **SQLAlchemy Session Lifecycle** | <ul><li>[ Completed] Map declarative SQLAlchemy models</li><li>[ Completed] Build request-scoped session dependency</li><li>[ Completed] Implement transaction rollback logic</li></ul> | Failed writes leave zero partial data; subsequent database operations succeed smoothly. | <ul><li>[ Completed] Database module</li><li>[ Completed] Repository functions</li><li>[ Completed] Transaction logs</li></ul> |
| **Day 13** | **Alembic Schema History** | <ul><li>[ Completed] Link Alembic to ORM metadata</li><li>[ Completed] Generate & apply initial migration auto-gen</li><li>[ Completed] Execute a minor schema column addition</li></ul> | Fresh target database upgrades seamlessly to the latest revision version. | <ul><li>[ Completed] Reviewed migrations</li><li>[ Completed] Upgrade execution logs</li><li>[ Completed] Schema comparison</li></ul> |
| **Day 14** | **SQL Queries & Activity History** | <ul><li>[ ] Write deterministic tasks-projects `JOIN` queries</li><li>[ ] Build audit activity table tracking state changes</li><li>[ ] Run `EXPLAIN` query plans on indexed vs unindexed columns</li></ul> | Task list fetches only expected scoped records; audit trail binds perfectly to target entities. | <ul><li>[ ] Optimized SQL queries</li><li>[ ] Activity migration script</li><li>[ ] Query plan comparison note</li></ul> |
| **Day 15** | **Database Integration Review** | <ul><li>[ ] Wipe out all volatile in-memory storage blocks</li><li>[ ] Add `/health` database liveness endpoints</li><li>[ ] Replay database drop, migration, and seed chain</li></ul> | Extracted tasks survive full API container restarts; duplicate/invalid references fail loudly. | <ul><li>[ ] Database-backed API code</li><li>[ ] Healthcheck logs</li><li>[ ] Full Week 3 review package</li></ul> |

---

## 🧪 Extra Supervised Practice (1:30 PM - 2:00 PM Daily Slot)

> ⚠️ *Note: Core tasks must be prioritized and resolved before addressing extension work.*

* **Objective:** Store one synthetic activity event using **MongoDB** and perform a comparative analysis against relational models.
* **Status:** ⬜ Not Started / 🟦 In Progress / 🟩 Completed

---

## 🏁 Weekly Onsite Evaluation Checklist
* [ ] **Live Demonstration:** Execute exactly one valid path case and one failure injection case on the live infrastructure.
* [ ] **Architectural Defense:** Explain one core engineering or transactional decision face-to-face without using external references.
* [ ] **Feedback Loop:** Log the supervisor's notes below and resolve at least one highlighted optimization item before Week 4 kicks off.

### 📝 Trainer Feedback Logs
* *To be filled during evaluation on Day 15...*
