# Day 24: Pagination Authorization & N+1 Query Investigation

## 🎯 Core Concepts Mastered
1. **Bounded Responses:** Preventing API denial-of-service by enforcing page limit ceilings (1–50) and rejecting invalid offsets.
2. **Resolver-Level Authorization:** Applying user ownership filters (`Task.owner_id == authenticated_user_id`) to every root query and ensuring missing or forbidden tasks resolve to `null`.
3. **N+1 Query Detection:** Hooking into the SQLAlchemy event bus (`before_cursor_execute`) to capture and count queries triggered during nested field resolution.

---

## 📊 N+1 Query Analysis & Architectural Mitigation

### What Was Observed in the Lab:
When resolving a list of 5 tasks with nested `project` data:
```graphql
query {
  tasks(limit: 5) {
    items {
      id
      title
      project { id name }
    }
  }
}
```
The execution engine performed:
1. `SELECT count(...)` (Total count)
2. `SELECT * FROM tasks WHERE owner_id = 1 LIMIT 5` (1 Query for tasks)
3. `SELECT * FROM projects WHERE id = ?` (5 Separate Queries, one per task)
**Total: 7 SQL Queries** for a single HTTP request of 5 records.

### How to Mitigate in Production:
1. **Eager Loading with `selectinload` / `joinedload`:**
   In SQLAlchemy, configuring `selectinload(Task.project)` batches project IDs into a single `SELECT * FROM projects WHERE id IN (?, ?, ?)` reducing the query count from $N+1$ to 2.
2. **DataLoader Pattern:**
   In Ariadne, using `DataLoader` collates all project ID requests across the entire execution tick into a single batched loader function.

---

## 🧪 Acceptance Check

Run the test suite:
```powershell
python test_day24.py
```

### Verified Criteria:
- [x] Limit ceiling: Requesting > 50 items raises GraphQLError.
- [x] Negative offset: Negative values are rejected.
- [x] Multi-user privacy: Bob cannot see or query Alice's tasks.
- [x] N+1 Query tracker: Captured exact SQL query counts during nested resolution.
