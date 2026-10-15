# Day 03: Functions and Modules (Task Management Service)

##  Concept Overview
This project demonstrates the core software engineering practice of **Separation of Concerns (SoC)**. By separating pure business rules from the transport layer (CLI interface / Web framework inputs), the underlying logic remains modular, testable, and completely independent of how data is collected or sent.

---

##  Design Note

* **Business Logic Layer (`app/task_service.py`)**: Acts as the single source of truth for task processing. It enforces domain constraints, validates incoming values, and generates unique persistence models. To prevent side effects, **immutability** is strictly guarded; the incoming client payloads are never modified, and a fresh dictionary record is always explicitly returned.
* **Transport Layers**: 
  * **CLI Layer (`cli_caller.py`)**: A lightweight command-line script handling basic human string inputs, routing them to the business engine, and printing clean outputs.
  * **Web UI Layer (`app/main.py`)**: A multi-page web transport layer utilizing FastAPI and HTML forms. It maps web requests to the service layer and gracefully catches domain exceptions without application service crashes.

---

##  Project Architecture
Ensure your project files are structured as follows inside your working directory:
```text
Day 3/
└── app/
    ├── __init__.py       # Marks directory as an importable module
    ├── main.py           # Web transport layer wrapper
    ├── task_service.py   # Pure business logic core and exceptions
    └── simple_task.py #task function
    ]
        
```

---



### 3. Running the Multi-Page Web App
To boot up the application web interface, execute the module wrapper via standard Python:
```bash
python -m app.main
```


---

## ✅ Acceptance Check Scenarios

### Case 1: Successful Task Creation
* Input valid data structures (e.g., Title: `"Complete code submission"`, Priority: `4`).
* **Expected Result**: Success code status, a fully validated dictionary returned with an incremental integer system ID assigned, and the state structure left untouched.

### Case 2: Business Rule Validation Failure
* Input structural edge cases (e.g., Blank space strings or a priority number out of bounds like `7`).
* **Expected Result**: Core throws a custom `ValidationError`. The CLI printer or Web UI catches it cleanly and handles displaying the reason string explicitly to the consumer without system disruptions.
