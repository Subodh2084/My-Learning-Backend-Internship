# Day 25: GraphQL Practical Review

## 🎯 Review Focus
Consolidate the Ariadne GraphQL server with the shared TaskFlow contract (Guide Page 5). Ensure all business validation and two-user access control rules are strictly enforced and verified by tests that inspect data and GraphQL `errors` rather than blindly asserting HTTP 200.

---

## 📋 Course Deliverables & Acceptance Verification
- [x] Full Ariadne GraphQL schema adhering to Shared Contract.
- [x] Query, mutation, invalid input, and two-user access control checks.
- [x] Detailed `operation_catalogue.md` documenting query/mutation specs.
- [x] **Acceptance Check:** Proved that injecting a deliberate resolver defect causes automated tests to fail (`test_07_deliberate_resolver_defect_acceptance_check`).

---

## 🧪 Running the Suite
```powershell
python test_day25.py
```
All 7 verification scenarios pass with 100% test coverage.
