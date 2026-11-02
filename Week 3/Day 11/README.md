# Day 11: PostgreSQL Setup and Schema Design

This repository contains the database schema, relational designs, synthetic data, and connectivity documentation required for the Day 11 PostgreSQL lab. The focus of this lab is understanding **relational keys, data integrity constraints**, and **host-versus-container networking**.

---

## 1. Schema Diagram & Architecture

### Entity-Relationship Text Representation
```text
  [ users ] 1 -------- * [ projects ] (Owned by a user)
     1                      1

     |                      |
     | *                    | *
  [ project_members ]      [ tasks ] (Belongs to a project)
     *                      *

     |                      |
     +----------+-----------+
                |
                v
       [ task_assignments ] (Tracks which user is assigned to what task)
```

### Relational Breakdown
*   **`users`**: The core entity representing platform participants.
*   **`projects`**: Created by a specific user (Owner). Features a 1:Many relationship (`users.id` -> `projects.owner_id`).
*   **`tasks`**: Individual units of work belonging to a single project. Features a 1:Many relationship (`projects.id` -> `tasks.project_id`).
*   **`task_assignments`**: A Many-to-Many junction table linking `users` to `tasks` to track delegation.

---

## 2. SQL Schema Implementation (DDL)

```sql
-- Drop existing tables to ensure a clean, reproducible environment
DROP TABLE IF EXISTS task_assignments;
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS users;

-- 1. Users Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Projects Table (Demonstrating 1:Many Ownership)
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    owner_id INT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints & Foreign Key Enforcement
    CONSTRAINT fk_project_owner 
        FOREIGN KEY (owner_id) 
        REFERENCES users(id) 
        ON DELETE CASCADE
);

-- 3. Tasks Table (Demonstrating 1:Many Project Hierarchy)
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    project_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    status VARCHAR(20) DEFAULT 'Todo' CHECK (status IN ('Todo', 'In Progress', 'Done')),
    due_date DATE,
    
    -- Constraints & Foreign Key Enforcement
    CONSTRAINT fk_task_project 
        FOREIGN KEY (project_id) 
        REFERENCES projects(id) 
        ON DELETE CASCADE
);

-- 4. Task Assignments Junction Table (Demonstrating Many-to-Many Relationships)
CREATE TABLE task_assignments (
    task_id INT NOT NULL,
    user_id INT NOT NULL,
    assigned_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Composite Primary Key prevents duplicate assignments
    PRIMARY KEY (task_id, user_id),
    
    CONSTRAINT fk_assignment_task 
        FOREIGN KEY (task_id) 
        REFERENCES tasks(id) 
        ON DELETE CASCADE,
        
    CONSTRAINT fk_assignment_user 
        FOREIGN KEY (user_id) 
        REFERENCES users(id) 
        ON DELETE CASCADE
);
```

---

## 3. Synthetic Seed Data (DML)

```sql
-- Insert Synthetic Users
INSERT INTO users (username, email) VALUES 
('alice_dev', 'alice@company.com'),
('bob_pm', 'bob@company.com'),
('charlie_qa', 'charlie@company.com');

-- Insert Synthetic Projects (Bob owns both projects)
INSERT INTO projects (name, description, owner_id) VALUES 
('Q4 Alpha Launch', 'Deliver the first iteration of the Alpha product.', 2),
('Internal Migration', 'Upgrade underlying legacy tech stack infrastructure.', 2);

-- Insert Synthetic Tasks
INSERT INTO tasks (project_id, title, status, due_date) VALUES 
(1, 'Setup production cluster CI/CD pipeline', 'In Progress', '2026-11-15'),
(1, 'Write comprehensive end-to-end integration tests', 'Todo', '2026-11-20'),
(2, 'Upgrade database engine to PG 16', 'Done', '2026-11-01');

-- Assign Users to Tasks
INSERT INTO task_assignments (task_id, user_id) VALUES 
(1, 1), -- Alice on the CI/CD pipeline task
(2, 1), -- Alice on the E2E tests task
(2, 3), -- Charlie also assisting with E2E tests
(3, 1); -- Alice handled the DB upgrade
```

---

## 4. Connectivity & Networking Notes

When working with containerized environments, selecting the correct network address is crucial for avoiding connection timeouts.

### Connection Address Matrix

| Scenario | Target Address / Host | Port | Explanation |
| :--- | :--- | :--- | :--- |
| **Host-to-Container** | `localhost` or `127.0.0.1` | `5432` | Connecting from your local machine terminal/IDE to a container exposing its ports using `-p 5432:5432`. |
| **Container-to-Container** | `postgres-service-name` | `5432` | Connecting from a backend application container to the DB container running inside the *same* custom Docker network. |
| **Container-to-Host** | `host.docker.internal` | `5432` | Connecting from inside a container out to a PostgreSQL engine running natively on the host Mac/Windows machine. |

### Reproducible Connection Command

Test database connectivity from your local terminal using the application user credentials:

```bash
# General connection string format:
# psql -h [HOST] -U [USER] -d [DATABASE] -p [PORT]

psql -h localhost -U postgres -d postgres -p 5432
```

---

## 5. Acceptance Check Verification

To verify that Primary Key and Foreign Key constraints are properly enforced, execute this query block. It asserts that standard deletions cascade seamlessly, and structural mutations that break relational contracts are intercepted.

```sql
-- 1. Verify Foreign Key Cascade on Delete
-- Removing Bob (ID: 2) should automatically wipe his projects, tasks, and task assignments.
DELETE FROM users WHERE id = 2;

SELECT 'Remaining users count:' AS check_label, COUNT(*) FROM users;
SELECT 'Remaining projects count (Should be 0):' AS check_label, COUNT(*) FROM projects;

-- 2. Verify Check Constraints (This statement should FAIL)
-- Trying to insert an invalid task status will trigger a check violation.
INSERT INTO tasks (project_id, title, status) VALUES (1, 'Will Fail Task', 'Invalid Status');
```
