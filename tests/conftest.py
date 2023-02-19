from pytest_factoryboy import register

from factories import AdFactory, UserFactory

pytest_plugins = 'tests.fixtures'

register(AdFactory)
register(UserFactory)
