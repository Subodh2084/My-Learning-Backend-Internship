# Day 27: Read Consistency After Writes

## 🎯 Objective
Ensure that reads following create, update, and delete mutations always reflect fresh state, even when an aggressive caching layer is applied.

---

## 🔍 Observed Stale Read vs Cache Invalidation

### Stale Read Phenomenon:
1. Client calls `GET /tasks` -> Cache populated with `[Task 1]`.
2. Client calls `POST /tasks` -> `Task 2` inserted into Database.
3. If cache is not invalidated, subsequent `GET /tasks` returns `[Task 1]` from cache.
4. Result: Data inconsistency and user confusion.

### Cache Invalidation Solution:
On any mutation (`POST`, `PATCH`, `DELETE`), all cache keys for the owning user (`user:{owner_id}:tasks:*`) are evicted. The very next read triggers a clean cache miss and reads fresh records from the database.

---

## 🧪 Acceptance Check

Run the consistency suite:
```powershell
python test_day27.py
```
- [x] Stale read reproduced and demonstrated when invalidation is turned off.
- [x] Read-after-write consistency guaranteed when invalidation is active.
- [x] Tested against local TTL cache fixture (Redis adapter contract equivalent).
