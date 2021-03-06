from pytest import fixture
from graphql import build_schema, graphql
from integrark.application.services import QueryService
from integrark.core.common import Solution, IntegrationImporter
from integrark.core.query import GraphqlQueryService, GraphqlSchemaLoader


@fixture
def schema_loader() -> GraphqlSchemaLoader:
    class MockGraphqlSchemaLoader(GraphqlSchemaLoader):
        def load(self):
            content = """
            type Doctor {
                name: String!
                specialty: String!
                age: Int
            }

            type Query {
                doctors: [Doctor]
                veterinary: Doctor
            }
            """
            return build_schema(content)

    return MockGraphqlSchemaLoader('/tmp/fake')


@fixture
def integration_importer() -> IntegrationImporter:
    class QuerySolution(Solution):
        type = 'Query'

        async def resolve__doctors(self, parent, info):
            return [
                {'name': 'Hugo', 'specialty': 'Cardiology'},
                {'name': 'Paco', 'specialty': 'Psychiatry'},
                {'name': 'Luis', 'specialty': 'Oncology'}
            ]

        async def resolve__veterinary(self, parent, info):
            raise Exception('The veterinary field has not been implemented.')

    class DoctorSolution(Solution):
        type = 'Doctor'

    class MockIntegrationImporter(IntegrationImporter):
        def load(self):
            self.solutions = [
                QuerySolution(),
                DoctorSolution()
            ]
            self.dataloaders_factory = lambda context: {}

    integration_importer = MockIntegrationImporter('/tmp/fake')
    integration_importer.load()
    return integration_importer


@fixture
def query_service(schema_loader, integration_importer) -> GraphqlQueryService:
    return GraphqlQueryService(schema_loader, integration_importer)


@fixture
def schema():
    content = """
    type Student {
        name: String!
        age: Int!
    }

    type Query {
        students: [Student]
    }
    """
    return build_schema(content)


@fixture
def students():
    return [
        {'name': 'Esteban', 'age': 30},
        {'name': 'Gabriel', 'age': 27},
        {'name': 'Valentina', 'age': 35},
    ]


@fixture
def solutions(students):
    class StudentSolution(Solution):
        type = 'Student'

    class QuerySolution(Solution):
        type = 'Query'

        async def resolve__students(self, parent, info):
            return students

    return [
        QuerySolution(),
        StudentSolution()
    ]


def test_graphql_query_service(query_service):
    assert issubclass(GraphqlQueryService, QueryService)
    assert isinstance(query_service, GraphqlQueryService)


async def test_graphql_query_service_run(query_service):
    query = """
    {
        doctors {
            specialty
        }
    }
    """

    result = await query_service.run(query)

    assert result.data == {
        'doctors': [
            {'specialty': 'Cardiology'},
            {'specialty': 'Psychiatry'},
            {'specialty': 'Oncology'}
        ]
    }
    assert result.errors is None


async def test_graphql_query_service_bind_schema(
        query_service, schema, solutions, students):

    schema = query_service._bind_schema(schema, solutions)

    query = """
    {
        students {
            name
            age
        }
    }
    """

    result = await graphql(schema, query)

    assert result.data['students'] == students
    assert result.errors is None


async def test_graphql_query_service_run_location_errors(query_service):
    query = """
    {
        doctors {
            name
            address
        }
    }
    """

    result = await query_service.run(query)

    assert result.data is None
    assert result.errors == [
        {'message': "Cannot query field 'address' on type 'Doctor'.",
         'locations': [{'line': 5, 'column': 13}], 'path': None}]


async def test_graphql_query_service_run_path_errors(query_service):
    query = """
    {
        doctors {
            name
        }
        veterinary {
            name
        }
    }
    """

    result = await query_service.run(query)

    assert result.data == {
        'doctors': [
            {'name': 'Hugo'},
            {'name': 'Paco'},
            {'name': 'Luis'}
        ],
        'veterinary': None
    }

    assert result.errors == [
        {'message': 'The veterinary field has not been implemented.',
         'locations': [{'line': 6, 'column': 9}],
         'path': ['veterinary']}
    ]
