from aiohttp import web


async def test_root(app) -> None:
    response = await app.get('/')

    content = await response.text()

    assert response.status == 200
    assert 'Integrark' in await response.text()


async def test_graphql_get(app) -> None:
    response = await app.get('/graphql')

    content = await response.text()

    assert response.status == 200
    assert 'GraphQL Playground' in await response.text()


async def test_graphql_post(app) -> None:
    response = await app.post('/graphql', data='{}')

    content = await response.text()

    assert response.status == 200
    assert "{}" in await response.text()
