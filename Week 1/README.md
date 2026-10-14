# README: Week 1 Project Foundation Master Checklist

This repository tracks the foundational setup, validation logic, and decoupled business services for the backend development internship.

---

## 📋 Week 1 Master Tracker & Syllabus Reference

| Day Tracking | Target Milestone / Module | Business Rules & Component Tasks | Required Core Reading & Concept Focus | Required Terminal Command / Check | Deliverable Verification | Status |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: |
| **DAY 01** | **Environment & Repo** | Record OS, Python, and Git version metrics | **Interpreter Selection & Isolated Dependencies:** How binaries execute scripts and prevent version collisions. | `python --version` <br> `git --version` | Verified workspace log file | Complete |
| **DAY 01** | **Environment & Repo** | Build app, tests, docs, and scripts directories | **Project Roots & Setup Documentation:** Structuring code systematically from a common reference directory base. | `mkdir app tests docs scripts` | Structural integrity verification | Complete |
| **DAY 01** | **Environment & Repo** | Isolate dependencies using a local virtual environment | **Reproducible Environments:** Creating fresh sandboxed runtime states using predictable deployment steps. | `python -m venv venv` | Active workspace shell indicator | Complete |
| **DAY 01** | **Environment & Repo** | Configure version control filters to avoid secret leaks | **Git Ignore Protocol:** Strategies for filtering background configurations out of public upstream trees. | `cat .gitignore` | Active block on local `.env` | Complete |
| **DAY 02** | **Values & Validation** | Code strict validation parameters for incoming titles | **Strings, Lengths, & Enforcements:** Strip whitespace and reject data leaks using character evaluations. | `python -m app.validators` | Rejection of empty spaces/overflows | ⬜ Pending |
| **DAY 02** | **Values & Validation** | Code numerical range parsing for input priorities | **Numbers & Bounded Conditions:** Translating data inputs safely using deterministic logical boundaries. | `python -m app.validators` | Rejection of out-of-bounds integers | ⬜ Pending |
| **DAY 02** | **Values & Validation** | Document theoretical differences: Accepting vs Parsing | **Accepting vs. Parsing:** Differentiating passive type signature validation from deep data casting mutations. | *Write conceptual definitions* | Completed architectural log entry | ⬜ Pending |
| **DAY 02** | **Values & Validation** | Run boundary error assertions & trigger a breaking rule | **Collections & Assertions:** Handling data containers (`dict`, `list`) and asserting error behaviors. | *Execute local test script* | Confirmed traceback output match | ⬜ Pending |
| **DAY 03** | **Functions & Modules** | Move validation constraints into a standalone service | **Functions & Import Modules:** Packaging validation blocks into clean namespaces separate from transport systems. | `import app.validators` | Decoupled execution loop verification | ⬜ Pending |
| **DAY 03** | **Functions & Modules** | Build non-mutating task creation logic (Immutability) | **Immutability Architecture:** Ensuring data logic returns pristine clones without corrupting incoming references. | *Review memory/object updates* | Initial record state remains unchanged | ⬜ Pending |
| **DAY 03** | **Functions & Modules** | Map explicit custom domain exceptions onto validation faults | **Exceptions Management:** Throwing isolated domain interruptions cleanly to protect deep logic tracks. | `raise ValidationError` | App error isolation test | ⬜ Pending |
| **DAY 03** | **Functions & Modules** | Build a command-line script caller to trigger modules | **Transport Separation Principles:** Decoupling pure business logic files away from quick wrapper CLI runners. | `./scripts/run_caller.sh` | Execution works from project root | ⬜ Pending |
| **DAY 04** | **Types & Configuration** | Implement static type hinting throughout the task service | **Type Hints & Static Checks:** Annotating structural properties so misalignments are exposed before execution. | `mypy app/` | Type-checker returns zero errors | ⬜ Pending |
| **DAY 04** | **Types & Configuration** | Inspect application response to a deliberate type mismatch | **Static Linting Adjustments:** Reviewing type mismatch signals via background compile loops. | *Introduce bad type signature* | Capture linter/type error output | ⬜ Pending |
| **DAY 04** | **Types & Configuration** | Load environment values securely with fallback defaults | **Environment Variables Engine:** Ingesting values safely from disk spaces while enforcing fallback configurations. | `python -m app.config` | Verification of default parameters | ⬜ Pending |
| **DAY 04** | **Types & Configuration** | Verify environment templates contain no real secrets | **Secrets Safety Protocols:** Blocking private credential patterns while keeping template blueprints transparent. | `cat .env.example` | Clear placeholder values list | ⬜ Pending |
| **DAY 04** | **Types & Configuration** | Isolate changes on a feature branch and trigger a conflict | **Branches & Code Reviews:** Maintaining stability on main branches while performing atomic target checks. | `git diff main feature/day-04` | Diff review and resolved conflict | ⬜ Pending |
| **DAY 05** | **Foundation Review** | Wipe local environment and rebuild from documentation | **Reproducibility Checks:** Erasing current working dependencies to dry-test step logs for fresh setups. | *Follow environment re-creation steps* | Clean, working standalone runtime | ⬜ Pending |
| **DAY 05** | **Foundation Review** | Write an independent, net-new validation rule from scratch | **Boundary Implementation:** Coding a brand-new target constraint freely without copying existing solutions. | *Implement new domain constraint* | Dynamic validation execution proof | ⬜ Pending |
| **DAY 05** | **Foundation Review** | Review input/output schemas, errors, and Git history logs | **Commit Stream Verification:** Audit functions against schema limits and clean up commit tracks for clarity. | `git log --oneline` | Human-readable commit stream | ⬜ Pending |
| **WEEK REVIEW** | **Final Demonstration** | Run one valid case, one failure case, and record trainer comments | **Onsite Validation Drills:** Running code scenarios live while talking through core logic without notes. | Live demo on the last working day | Logged corrections for Week 2 | ⬜ Pending |
| **EXTENSION WORK** | **Supervised Practice** | Compare Poetry with venv workflows during the 1:30 PM slot | **Tooling Tradeoffs (30-Min Slot):** Assessing lockfile tracking differences vs speed across platforms. | *Write tradeoff log sheet* | Documented package tool matrix | ⬜ Pending |

---

## 📁 Repository Reference Layout

```text
.
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── exceptions.py
│   └── validators.py
├── tests/
│   └── test_validators.py
├── docs/
│   └── architecture.md
├── scripts/
│   └── run_caller.sh
├── .env.example
├── .gitignore
└── requirements.txt
```
