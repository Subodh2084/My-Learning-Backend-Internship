# Day 28: Background Work & Job States

## 🎯 Focus
1. Modeling discrete job states: `PENDING`, `RUNNING`, `SUCCESS`, and `FAILED`.
2. Examining the trade-offs between in-process background tasks (`starlette.background.BackgroundTasks`) vs durable external queues ([ARQ](https://github.com/samuelcolvin/arq) / Redis).
3. Demonstrating that unexecuted in-process jobs are lost permanently on worker restart.

---

## ⚖️ In-Process vs External Queue Comparison

| Capability | FastAPI `BackgroundTasks` | ARQ + Redis Queue |
| :--- | :--- | :--- |
| **Execution Environment** | Same ASGI process (event loop / thread) | Dedicated external worker processes |
| **Durability on Restart** | ❌ Lost immediately if server restarts | ✅ Persisted in Redis until acknowledged |
| **Retries & Backoff** | ❌ None (exception kills task) | ✅ Configurable retry counts & backoff |
| **Resource Isolation** | ❌ CPU spikes affect HTTP response latency | ✅ Workload isolated from web server |

---

## 🧪 Acceptance Check

Run the test suite:
```powershell
python test_day28.py
```
- [x] State transitions verified (`PENDING` -> `RUNNING` -> `SUCCESS`).
- [x] Errors captured and recorded with diagnostics (`FAILED`).
- [x] Durability limit demonstrated via process crash simulation.
