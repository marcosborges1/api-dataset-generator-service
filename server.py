# server.py
import uvicorn
from ariadne import QueryType, make_executable_schema
from ariadne.asgi import GraphQL
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from my_graphql.schemas.index import type_defs
from my_graphql.resolvers.index import resolve_generate_dataset

# Ariadne setup
query = QueryType()
query.set_field("generateDataset", resolve_generate_dataset)
schema = make_executable_schema(type_defs, query)
graphql_app = GraphQL(schema, debug=True)

# Define the routes for the app
routes = [
    Route("/", graphql_app),
    Mount("/data", StaticFiles(directory="data"), name="static"),
]

# Create the Starlette app with the defined routes
app = Starlette(routes=routes)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=4002)
