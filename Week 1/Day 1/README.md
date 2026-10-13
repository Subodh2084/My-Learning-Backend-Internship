# Day 01: Environment and Repository Blueprint

This repository contains the complete environment structure, runtime baseline, and isolation configuration required for predictable, reproducible local Python development.

##  Core Concepts
*   **Interpreter Selection:** The specific `python.exe` binary engine used to run the application. Forcing VS Code to explicitly target our local workspace environment prevents the IDE from accidentally invoking unmanaged system runtimes or global packages.
*   **Isolated Dependencies:** Sandboxing external software libraries (like `fastapi` and `pydantic`) within a local workspace folder (`.venv`). This guarantees our project configurations never clash with other environments on the machine.
*   **Project Roots:** The highest-level root folder anchoring our version history tree (`.git\`), layout folders, configurations, and internal path resolutions to guarantee complete workspace portability.
*   **Reproducible Setup:** Utilizing structured dependency lockfiles (`requirements.txt`) and unified terminal recipes so that any machine can mirror this exact execution context with zero variation.
---
## version Check 

```cmd
::Windows version os version 
ver
::python version
python --version
::git version
git --version
Version is present inside version folder
```
---

##  Project Architecture
The project workspace is partitioned into specific semantic boundaries:
*   `app/`     : Core application logic, routers, database schemas, and service-layer validation pipelines.
*   `tests/`   : Functional, unit, and structural execution assertions.
*   `docs/`    : System specifications, baseline manifests, and API manuals.
*   `scripts/` : Utility deployment, environmental scaffolding, or database maintenance scripts.

---

##  Windows CMD Setup & Reproducible Installation

### 1. Fresh Workspace Initialization
To recreate this isolated sandbox environment from scratch in a fresh Windows Command Prompt (`cmd.exe`), navigate to your project root folder and execute:
```cmd
:: Create isolation boundary, activate local runtime, and upgrade the installer core
python -m venv .venv && call .venv\Scripts\activate && python -m pip install --upgrade pip

:: Deploy explicit and transitive project dependency structures
pip install -r requirements.txt
```

### 2. Standard Reinstallation Routine
If the environment is already initialized and you only need to sync package definitions, run:
```cmd
python -m pip install --upgrade pip && pip install -r requirements.txt
```

---

##  Verification & Acceptance Check
To confirm strict execution isolation, open a clean `cmd.exe` terminal and run:

1.  **Activate Environment:**
    ```cmd
    call .venv\Scripts\activate.bat
    ```
2.  **Verify Interpreter Target Path:**
    ```cmd
    where python
    ```
    *Acceptance Criteria: The first resolution path must point directly inside your localized project root `\.venv\Scripts\python.exe`.*
3.  **Verify Environmental Cleanliness:**
    ```cmd
    pip list
    ```
    *Acceptance Criteria: The output must purely return the specified baseline stack (FastAPI 0.143.0, Pydantic, Uvicorn, and related sub-dependencies) with zero unmanaged global modules visible.*

---

##  Running the Server Environment
Once code assets are configured inside the execution tree, run the development microservice via:
```cmd
uvicorn app.main:app --reload
```