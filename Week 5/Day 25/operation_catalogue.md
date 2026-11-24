# Operation Catalogue: TaskFlow GraphQL API (Day 25)

Base URL: `http://localhost:8000/graphql`  
Authentication: `Authorization: Bearer <token>`

---

## 1. Query: Current User (`me`)
```graphql
query GetCurrentUser {
  me {
    id
    email
  }
}
```
**Headers:** `Authorization: Bearer token-alice-secret`  
**Sample Response:**
```json
{
  "data": {
    "me": {
      "id": "1",
      "email": "alice@taskflow.dev"
    }
  }
}
```

---

## 2. Query: Bounded Tasks (`tasks`)
```graphql
query ListTasks($limit: Int, $offset: Int, $status: TaskStatus) {
  tasks(limit: $limit, offset: $offset, status: $status) {
    total
    items {
      id
      title
      priority
      status
      ownerId
    }
  }
}
```
**Variables:**
```json
{
  "limit": 10,
  "offset": 0,
  "status": "OPEN"
}
```

---

## 3. Query: Single Task (`task`)
```graphql
query GetTask($id: ID!) {
  task(id: $id) {
    id
    title
    priority
    status
    ownerId
  }
}
```
**Note:** Missing or forbidden tasks resolve cleanly to `null` as defined in the course contract.

---

## 4. Mutation: Create Task (`createTask`)
```graphql
mutation CreateNewTask($input: TaskInput!) {
  createTask(input: $input) {
    id
    title
    priority
    status
    ownerId
  }
}
```
**Variables:**
```json
{
  "input": {
    "title": "Set up automated test pipeline",
    "priority": "HIGH"
  }
}
```

---

## 5. Mutation: Update Task (`updateTask`)
```graphql
mutation UpdateExistingTask($id: ID!, $input: TaskUpdate!) {
  updateTask(id: $id, input: $input) {
    id
    title
    priority
    status
  }
}
```
**Variables:**
```json
{
  "id": "1",
  "input": {
    "status": "DONE"
  }
}
```

---

## 6. Mutation: Delete Task (`deleteTask`)
```graphql
mutation RemoveTask($id: ID!) {
  deleteTask(id: $id) {
    id
    deleted
  }
}
```
