import aiohttp_cors
from pathlib import Path
from jinja2 import FileSystemLoader
from aiohttp import web
from aiohttp_jinja2 import setup
from injectark import Injectark
from .api import create_api
from .middleware import MIDDLEWARES


def create_app(config, injector: Injectark) -> web.Application:

    app = web.Application(middlewares=MIDDLEWARES)
    templates = str(Path(__file__).parent / 'templates')
    setup(app, loader=FileSystemLoader(templates))
    create_api(app, injector)
    enable_cors(app)

    return app


def run_app(app: web.Application, port=4321) -> None:
    web.run_app(app, port=port)


def enable_cors(app: web.Application) -> None:
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*"
        )
    })

    # Configure CORS on all routes.
    for route in list(app.router.routes()):
        cors.add(route)
