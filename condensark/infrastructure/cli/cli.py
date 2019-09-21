import sys
import json
from argparse import ArgumentParser, Namespace
from injectark import Injectark
from typing import List
from ..core import Config


class Cli:
    def __init__(self, config: Config, resolver: Injectark) -> None:
        self.config = config
        self.resolver = resolver
        self.parser = ArgumentParser('Condensark')

    def run(self, argv: List[str]):
        args = self.parse(argv)
        args.func(argv)

    def parse(self, argv: List[str]) -> Namespace:
        subparsers = self.parser.add_subparsers()

        # Serve
        serve_parser = subparsers.add_parser(
            'serve', help='Start HTTP server.')
        serve_parser.set_defaults(func=self.serve)

        if len(argv) == 0:
            self.parser.print_help()
            self.parser.exit()

        return self.parser.parse_args(argv)

    def serve(self, args: Namespace) -> None:
        print('...SERVE:::', args)
