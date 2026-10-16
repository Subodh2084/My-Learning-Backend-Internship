# Day 04: Types, Configuration, and Git Architecture

## Overview
This repository contains the completion log and submission artifacts for the Day 04 Lab. The core objectives demonstrate static type validation interfaces in Python, secure configuration lifecycle management using environment abstraction patterns, and Git branch conflict resolution.

---

## Project Structure
```text
Day 4/
├── .env                # Local secrets (Ignored by Git)
├── .env.example        # Public configuration blueprint template

├── typeExample.py     # Strongly typed task service interface
└── README.md           # Project submission and documentation
```

---

## 1. Typed Task Service (`task_service.py`)

This script defines explicit structural schemas using Python's native `typing` tools (`TypedDict`). It contains an operational service along with an intentional parameter mismatch for validation tracking.

```python
# task_service.py
from typing import List, Literal, TypedDict

# Structural schemas for strong engine interface definitions
class Task(TypedDict):
    id: int
    title: str
    completed: bool

class AppConfig(TypedDict):
    port: int
    environment: Literal['development', 'production', 'staging']

class TaskService:
    def __init__(self) -> None:
        self.tasks: List[Task] = []

    # Strongly typed signature enforcing strict validation
    def create_task(self, id: int, title: str) -> Task:
        new_task: Task = {
            "id": id,
            "title": title,
            "completed": False
        }
        self.tasks.append(new_task)
        return new_task


service = TaskService()


service.create_task("People", "This is title")
```

### Static Type Checker Validation
Because Python evaluates parameters dynamically at runtime, a external static analyzer (`mypy`) must be invoked to catch structural mismatches. 

**Execution Command:**
```bash
mypy task_service.py
```

**Diagnostic Error Output Captured:**
```text
task_service.py:31: error: Argument 1 to "create_task" of "TaskService" has incompatible type "str"; expected "int"
Found 1 error in 1 file (checked 1 source file)
```

---

## 2. Configuration Strategy & Environment Sandboxing

To ensure target systems scale securely, real credentials are bound locally inside an ignored `.env` shell while exposing structural variable frameworks via an untracked blueprint.

### Environment Management Shells

* **`.env` (Local Workspace Scope - Secret Data Hidden)**
  ```ini
  PORT=8080
  ENVIRONMENT=development
  DATABASE_SECRET_KEY=super_secret_production_key_12345
  ```

* **`.env.example` (Tracked Repository Layer - Clean Reference Only)**
  ```ini
  PORT=3000
  ENVIRONMENT=development
  DATABASE_SECRET_KEY=YOUR_SECRET_KEY_HERE
  ```

### Safe-Default Reader Engine (`config.py`)
This pipeline parses properties safely, converting numeric fields and ensuring the strings map exactly to supported environment states.

```python
import os

def load_config() -> dict:
    port_raw = os.getenv("PORT", "3000")
    
    # Safe structural cast with integer fallback defaults
    try:
        port = int(port_raw)
    except ValueError:
        port = 3000
        
    # Boundary restriction framework for validation matching
    environment = os.getenv("ENVIRONMENT", "development")
    if environment not in ['development', 'production', 'staging']:
        environment = 'development'
        
    return {
        "port": port,
        "environment": environment
    }

config = load_config()
print(f"Running on Port: {config['port']} inside [{config['environment']}] environment.")
```

---

## 3. Git Branching, Code Reviews, & Merge Conflict Log

The terminal ledger log tracking features isolation branches, explicit history state evaluations via diff parameters, and manual resolution maps.

```bash
# Step A: Lock environment settings inside the ignore database
$ echo ".env" >> .gitignore
$ git status
# On branch main
# Changes not staged for commit:
#   modified:   .gitignore
# Untracked files:
#   .env.example
#   config.py
#   task_service.py
# (.env is confirmed excluded successfully)

# Step B: Spin up a designated feature track
$ git checkout -b feature/update-config
Switched to a new branch 'feature/update-config'

# [Updated default fallback parameter to 5000 in config.py]
$ git commit -am "Update default fallback port to 5000"

# Step C: Review branch variances via reviewable diff comparison
$ git diff main..feature/update-config
diff --git a/config.py b/config.py
index e69de29..92b3a1a 100644
--- a/config.py
+++ b/config.py
@@ -5,3 +5,3 @@ def load_config() -> dict:
-    port_raw = os.getenv("PORT", "3000")
+    port_raw = os.getenv("PORT", "5000")
     try:

# Step D: Induce conflicting upstream structural changes on main
$ git checkout main
Switched to branch 'main'
# [Updated default fallback parameter to 9000 in config.py]
$ git commit -am "Update main branch default fallback port to 9000"

# Step E: Trigger structural collision and process resolution
$ git merge feature/update-config
Auto-merging config.py
CONFLICT (content): Merge conflict in config.py
Automatic merge failed; fix conflicts and then commit the result.

$ cat config.py
    port_raw = os.getenv("PORT", "9000")

# [Resolved manually by keeping 5000 and purging conflict boundary markers]
$ git add config.py
$ git commit -m "Merge branch 'feature/update-config' and resolve port conflict"
```

---

## Acceptance Check Status Verification
* **`.env` Target Verification:** **[PASSED]** Excluded via configuration rule inside `.gitignore`.
* **`.env.example` Context Integrity:** **[PASSED]** Safe placeholders are verified with zero raw data or real operational credentials.
