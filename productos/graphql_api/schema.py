"""Ensamblaje del esquema GraphQL."""

import strawberry

from productos.graphql_api.mutations import Mutation
from productos.graphql_api.queries import Query

schema = strawberry.Schema(query=Query, mutation=Mutation)
