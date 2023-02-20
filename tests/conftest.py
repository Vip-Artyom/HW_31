from pytest_factoryboy import register

from tests.factories import UserFactory, CategoryFactory, AdFactory

pytest_plugins = "tests.fixtures"

register(CategoryFactory)
register(UserFactory)
register(AdFactory)
