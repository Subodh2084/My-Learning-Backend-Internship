# Day 26: Dependency Timeouts & Cache Design

## 🎯 Focus
1. Establishing strict, bounded timeout budgets to isolate failing dependencies.
2. Designing tenant-safe, owner-partitioned cache keys (`user:{owner_id}:tasks:page:{offset}:{limit}`).
3. Implementing and verifying a local TTL cache fixture that guarantees key eviction at the exact expiration boundary.

---

## ⏱️ Timeout Budget Matrix

| Dependency | Timeout Setting | Failure Action |
| :--- | :--- | :--- |
| **Database Pool Checkout** | 3.0s | Raise `503 Service Unavailable` |
| **SQL Query Execution** | 2.0s | Abort statement, log `SLOW_QUERY_ALERT` |
| **Cache Operation** | 0.5s | Fallback to database query (circuit pass-through) |
| **External HTTP Calls** | 2.5s | Abort request, return graceful fallback response |

---

## 🧪 Acceptance Check

Run the test suite:
```powershell
python test_day26.py
```
- [x] Timeouts confirmed bounded within safety limits.
- [x] Owner key isolation verified; Alice and Bob cache partitions do not leak.
- [x] TTL expiration verified at boundary.
