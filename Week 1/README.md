# README: Week 1 Project Foundation Master Checklist

This repository tracks the foundational setup, validation logic, and decoupled business services for the backend development internship. 

---

## 📋 Week 1 Master Tracker

| Day Tracking | Target Milestone / Module | Business Rules & Component Tasks | Required Terminal Command / Check | Deliverable Verification | Status |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **DAY 01** | **Environment & Repo** | Record OS, Python, and Git version metrics | `python3 --version` <br> `git --version` | Verified workspace log file | ⬜ Pending |
| **DAY 01** | **Environment & Repo** | Build app, tests, docs, and scripts directories | `mkdir app tests docs scripts` | Structural integrity verification | ⬜ Pending |
| **DAY 01** | **Environment & Repo** | Isolate dependencies using a local virtual environment | `python3 -m venv venv` | Active workspace shell indicator | ⬜ Pending |
| **DAY 01** | **Environment & Repo** | Configure version control filters to avoid secret leaks | `cat .gitignore` | Active block on local `.env` | ⬜ Pending |
| **DAY 02** | **Values & Validation** | Code strict validation parameters for incoming titles | `python -m app.validators` | Rejection of empty spaces/overflows | ⬜ Pending |
| **DAY 02** | **Values & Validation** | Code numerical range parsing for input priorities | `python -m app.validators` | Rejection of out-of-bounds integers | ⬜ Pending |
| **DAY 02** | **Values & Validation** | Document theoretical differences: Accepting vs Parsing | *Write conceptual definitions* | Completed architectural log entry | ⬜ Pending |
| **DAY 02** | **Values & Validation** | Run boundary error assertions & trigger a breaking rule | *Execute local test script* | Confirmed traceback output match | ⬜ Pending |
| **DAY 03** | **Functions & Modules** | Move validation constraints into a standalone service | `import app.validators` | Decoupled execution loop verification | ⬜ Pending |
| **DAY 03** | **Functions & Modules** | Build non-mutating task creation logic (Immutability) | *Review memory/object updates* | Initial record state remains unchanged | ⬜ Pending |
| **DAY 03** | **Functions & Modules** | Map explicit custom domain exceptions onto validation faults | `raise ValidationError` | App error isolation test | ⬜ Pending |
| **DAY 03** | **Functions & Modules** | Build a command-line script caller to trigger modules | `./scripts/run_caller.sh` | Execution works from project root | ⬜ Pending |
| **DAY 04** | **Types & Configuration** | Implement static type hinting throughout the task service | `mypy app/` | Type-checker returns zero errors | ⬜ Pending |
| **DAY 04** | **Types & Configuration** | Inspect application response to a deliberate type mismatch | *Introduce bad type signature* | Capture linter/type error output | ⬜ Pending |
| **DAY 04** | **Types & Configuration** | Load environment values securely with fallback defaults | `python -m app.config` | Verification of default parameters | ⬜ Pending |
| **DAY 04** | **Types & Configuration** | Verify environment templates contain no real secrets | `cat .env.example` | Clear placeholder values list | ⬜ Pending |
| **DAY 04** | **Types & Configuration** | Isolate changes on a feature branch and trigger a conflict | `git diff main feature/day-04` | Diff review and resolved conflict | ⬜ Pending |
| **DAY 05** | **Foundation Review** | Wipe local environment and rebuild from documentation | *Follow environment re-creation steps* | Clean, working standalone runtime | ⬜ Pending |
| **DAY 05** | **Foundation Review** | Write an independent, net-new validation rule from scratch | *Implement new domain constraint* | Dynamic validation execution proof | ⬜ Pending |
| **DAY 05** | **Foundation Review** | Review input/output schemas, errors, and Git history logs | `git log --oneline` | Human-readable commit stream | ⬜ Pending |
| **WEEK REVIEW** | **Final Demonstration** | Run one valid case, one failure case, and record trainer comments | *Onsite live deployment* | Logged corrections for Week 2 | ⬜ Pending |
| **EXTENSION WORK** | **Supervised Practice** | Compare Poetry with venv workflows during the 1:30 PM slot | *Write tradeoff log sheet* | Documented package tool matrix | ⬜ Pending |

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
