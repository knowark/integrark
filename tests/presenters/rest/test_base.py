from aiohttp import web
from injectark import Injectark
from integrark.core import config
from integrark.factories import factory_builder
from integrark.presenters.rest import create_app, run_app
from integrark.presenters.rest import base as base_module


def test_create_app():
    config['factory'] = 'CheckFactory'
    factory = factory_builder.build(config)

    injector = Injectark(factory)

    app = create_app(config, injector)

    assert app is not None
    assert isinstance(app, web.Application)


async def test_run_app(monkeypatch):
    application = None
    called = None
    mock_application = web.Application()

    class MockWeb:
        async def _run_app(self, app, port):
            nonlocal called
            called = True
            nonlocal application
            application = app

    monkeypatch.setattr(
        base_module, 'web', MockWeb())

    await run_app(mock_application)

    assert called
    assert application == mock_application
