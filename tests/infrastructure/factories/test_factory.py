from condensark.infrastructure.core import TrialConfig, Config
from condensark.infrastructure.factories import build_factory, Factory


def test_build_factory():
    config = TrialConfig()

    factory = build_factory(config)

    assert isinstance(factory, Factory)


def test_factory_methods() -> None:
    methods = Factory.__abstractmethods__  # type: ignore

    assert '__init__' in methods
    assert Factory.extract is not None


def test_build_factory_multiple_factories() -> None:
    methods = Factory.__abstractmethods__  # type: ignore

    factories = [
        'MemoryFactory', 'TrialFactory']

    class MockConfig(Config):
        def __init__(self, name):
            self['factory'] = name

    for name in factories:
        config = MockConfig(name)
        factory = build_factory(config)
        assert type(factory).__name__ == name


def test_factory_extract() -> None:
    class MockFactory(Factory):
        def __init__(self, context):
            pass

        def _my_method(self):
            pass

    factory = MockFactory({})
    method = factory.extract('_my_method')

    assert method == factory._my_method
