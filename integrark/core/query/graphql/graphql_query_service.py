import logging
from typing import List, Dict, Any
from graphql import GraphQLSchema, GraphQLObjectType, graphql, format_error
from ....application.services import QueryService, QueryResult
from ...common import IntegrationImporter, Solution
from .graphql_schema_loader import GraphqlSchemaLoader


class GraphqlQueryService(QueryService):

    def __init__(self, schema_loader: GraphqlSchemaLoader,
                 integration_importer: IntegrationImporter) -> None:
        self.logger = logging.getLogger(__name__)
        self.schema = schema_loader.load()
        self.solutions = integration_importer.solutions
        self.schema = self._bind_schema(self.schema, self.solutions)

    async def run(self, query: str,
                  context: Dict[str, Any] = None) -> QueryResult:
        context = context or {}
        graphql_kwargs = context.pop('graphql', {'context_value': {}})
        graphql_context = graphql_kwargs['context_value']
        graphql_context.update({'dataloaders': {}})

        graphql_result = await graphql(self.schema, query, **graphql_kwargs)

        data = graphql_result.data
        errors = []
        for error in graphql_result.errors or []:
            self.logger.error(error, exc_info=error)
            errors.append(format_error(error))

        return QueryResult(data, errors or None)

    def _bind_schema(self, schema: GraphQLSchema,
                     solutions: List[Solution]) -> GraphQLSchema:

        solutions_map = {solution.type: solution for solution in solutions}
        custom_types = [type_ for type_ in schema.to_kwargs()['types']
                        if not type_.name.startswith('__')]

        for type_ in custom_types:
            if isinstance(type_, GraphQLObjectType):
                solution = solutions_map[type_.name]
                self.logger.debug(f' Binding solution: {solution} ')
                solution_type = schema.get_type(solution.type)
                assert solution_type
                fields = getattr(solution_type, 'fields', [])
                for name, field in fields.items():
                    field.resolve = solution.resolve(name)

        return schema
