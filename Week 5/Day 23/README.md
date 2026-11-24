# Day 23: Mutations and Shared Services

## 🎯 Overview
In Day 23, we implement mutations in Ariadne GraphQL while ensuring **absolute parity** with REST endpoints by sharing the domain service layer (`ItemService`). 

Neither REST route handlers nor GraphQL resolvers implement business logic directly. Instead, both act as thin transport gateways that call the shared domain service.

---

## 🏛️ Architecture & Clean Domain Separation

```
[REST Client]       --> [FastAPI Route /items]        \
                                                        --> [ItemService] --> [Domain Rules & Storage]
[GraphQL Client]    --> [Ariadne Resolvers /graphql]  /
```

### Shared Business Rules Enforced:
1. **Title Validation:** Trims leading/trailing whitespace. Must be between 5 and 80 characters.
2. **State Machine Transitions:**
   - `OPEN` -> `IN_PROGRESS`
   - `IN_PROGRESS` -> `OPEN` or `DONE`
   - `DONE` -> `IN_PROGRESS`
   - Any invalid jump (such as `OPEN` -> `DONE`) raises `DomainValidationError`.
3. **Resource Ownership:**
   - Every item stores `owner_id`.
   - Modifying or deleting an item requires `requesting_user_id == owner_id`.
   - Non-owners receive `DomainPermissionError` (HTTP 403 in REST, GraphQLError in GraphQL).

---

## 🧪 Acceptance Check & Test Execution

Run the parity test suite:
```powershell
python test_day23.py
```

### Verified Scenarios:
- [x] Valid task creation across REST and GraphQL mutations.
- [x] Rejection of short titles (< 5 characters) in both layers.
- [x] Rejection of illegal state transitions (OPEN to DONE) in both layers.
- [x] Enforcement of resource ownership; User B cannot modify or delete User A's tasks.
