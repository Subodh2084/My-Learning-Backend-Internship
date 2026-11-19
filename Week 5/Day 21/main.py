from fastapi import FastAPI
from ariadne import load_schema_from_path, make_executable_schema
from ariadne.asgi import GraphQL
from resolver import bindables

# 1. Load and validate the schema file
type_defs = load_schema_from_path("schema.graphql")

# 2. Bind Python resolvers to the schema
schema = make_executable_schema(type_defs, *bindables)

# 3. Mount Ariadne to FastAPI
app = FastAPI()
graphql_app = GraphQL(schema, debug=True)

app.mount("/graphql", graphql_app)
