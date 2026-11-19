from ariadne import QueryType, MutationType, ObjectType, EnumType
from graphql import GraphQLError

query = QueryType()
mutation = MutationType()
project_type = ObjectType("Project")
task_type = ObjectType("Task")

# Map GraphQL Enum directly to Python strings/enums
task_status = EnumType(
    "TaskStatus",
    {
        "TODO": "todo",
        "IN_PROGRESS": "in_progress",
        "DONE": "done",
    },
)

# --- Query Resolvers ---

@query.field("projects")
def resolve_projects(_, info, page):
    limit = page["limit"]
    offset = page["offset"]
    # Replace with your actual DB query; always return a list, never None
    return [
        {"id": "proj_1", "name": "FastAPI Migration", "owner_id": "usr_1"}
    ][offset : offset + limit]

@query.field("project")
def resolve_project(_, info, id):
    # Return None if not found (allowed because 'project(id: ID!): Project' is nullable)
    if id != "proj_1":
        return None
    return {"id": "proj_1", "name": "FastAPI Migration", "owner_id": "usr_1"}

# --- Nested Field Resolvers ---

@project_type.field("owner")
def resolve_project_owner(project_obj, info):
    # 'owner: User!' is non-nullable; raise an error if data integrity is broken
    owner = {"id": project_obj["owner_id"], "username": "dev_alex", "email": "alex@example.com", "createdAt": "2026-11-19"}
    if not owner:
        raise GraphQLError("Project owner not found.")
    return owner

@project_type.field("tasks")
def resolve_project_tasks(project_obj, info, limit=10, offset=0):
    # 'tasks: [Task!]!' must always return a list
    all_tasks = [
        {"id": "tsk_1", "title": "Setup Ariadne", "status": "in_progress", "project_id": "proj_1"}
    ]
    return [t for t in all_tasks if t["project_id"] == project_obj["id"]][offset : offset + limit]

# --- Mutation Resolvers ---

@mutation.field("createTask")
def resolve_create_task(_, info, input):
    # Ariadne automatically validates 'input' shape against CreateTaskInput before this runs
    new_task = {
        "id": "tsk_99",
        "title": input["title"],
        "description": input.get("description"),
        "status": "todo",
        "project_id": input["projectId"],
        "assigned_to_id": input.get("assignedToId"),
    }
    return new_task

bindables = [query, mutation, project_type, task_type, task_status]
