from nameko.testing.services import entrypoint_hook

from service import PrimeService


def pytest_configure(config):
    config.option.RABBIT_AMQP_URI = 'amqp://guest:guest@amqp:5672'
    config.option.RABBIT_API_URI = 'http://guest:guest@amqp:15672'
    return config


def test_blocking(container_factory, rabbit_config):
    container = container_factory(PrimeService, rabbit_config)
    container.start()

    with entrypoint_hook(container, 'blocking') as entrypoint:
        result = entrypoint(1, 10)
        assert result == [1, 2, 3, 5, 7]


def test_cooperative(container_factory, rabbit_config):
    container = container_factory(PrimeService, rabbit_config)
    container.start()

    with entrypoint_hook(container, 'cooperative') as entrypoint:
        result = entrypoint(1, 10)
        assert result == [1, 2, 3, 5, 7]
