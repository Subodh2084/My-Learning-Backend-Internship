# Week 5: GraphQL with Ariadne — Module Summary & Deliverables

## 🎯 Weekly Focus
Exposing a schema-first GraphQL API alongside existing REST endpoints while ensuring complete business logic parity and authorization consistency using [Ariadne](https://ariadnegraphql.org) and Python.

---

## 📊 Week 5 Sprint & Deliverables Tracker

| Day | Module / Concept | Task / Objective | Status | Artifact / Deliverable | Verified Checkpoint |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **Day 21** | **GraphQL Schema Design** | Schema-first types, inputs, bounded queries, and nullability rules. | Complete | `Week 5/Day 21/schema.graphql` | • Non-nullable fields guarded.<br>• Schema validation catches invalid shapes. |
| **Day 22** | **Ariadne Queries & Context** | Mount Ariadne ASGI, bind QueryType, build auth context with token. | Complete | `Week 5/Day 22/main.py` | • Context carries DB session & user.<br>• Unauthenticated requests return null. |
| **Day 23** | **Mutations & Shared Services** | Implement createTask, updateTask, deleteTask sharing domain service layer. | Complete | `Week 5/Day 23/main.py`<br>↳ `services/item_service.py` | • Title trim 5-80 chars enforced.<br>• State machine rules verified.<br>• Parity with REST verified. |
| **Day 24** | **Pagination & N+1 Problem** | Enforce bounded list limits (1-50), investigate N+1 SQL queries via event listener. | Complete | `Week 5/Day 24/test_day24.py`<br>↳ `query_tracker.py` | • Limits clamped to 50 max.<br>• N+1 query pattern captured & documented.<br>• Multi-user isolation verified. |
| **Day 25** | **GraphQL Practical Review** | End-to-end practical review, diagnosable error checks, deliberate defect test. | Complete | `Week 5/Day 25/test_day25.py`<br>↳ `operation_catalogue.md` | • Deliberate defect fails suite.<br>• Shared contract fully satisfied.<br>• Comprehensive operation catalog. |

---

## 💡 Key Architectural Insights
1. **Thin Transport Gateways:** Neither REST route handlers nor GraphQL resolvers should contain business logic. Both delegate to a shared domain service (`TaskService`).
2. **Diagnosable Errors vs HTTP 200:** GraphQL requests often return HTTP 200 even when operations fail. Tests must assert on `data` and inspect the `errors` payload.
3. **N+1 Avoidance:** In Ariadne, nested queries trigger $N+1$ database calls unless mitigated with SQLAlchemy eager loading (`selectinload`) or DataLoaders.
