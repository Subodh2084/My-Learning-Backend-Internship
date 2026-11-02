CREATE DATABASE management_db;

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE projects (
    project_id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    owner_id INT NOT NULL,
    CONSTRAINT fk_project_owner 
        FOREIGN KEY (owner_id) 
        REFERENCES users(user_id) 
        ON DELETE CASCADE
);


CREATE TABLE tasks (
    task_id SERIAL PRIMARY KEY,
    project_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'Todo' NOT NULL,
    assigned_to INT,
    CONSTRAINT fk_task_project 
        FOREIGN KEY (project_id) 
        REFERENCES projects(project_id) 
        ON DELETE CASCADE,
    CONSTRAINT fk_task_assignee 
        FOREIGN KEY (assigned_to) 
        REFERENCES users(user_id) 
        ON DELETE SET NULL,
    CONSTRAINT chk_status 
        CHECK (status IN ('Todo', 'In Progress', 'Done'))
);
