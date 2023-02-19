import factory.django

from users.models import Users
from ads.models import Ad, Category


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Users

    username = factory.Faker('name')
    password = 'password'
    role = 'admin'
    email = factory.Faker('email')
    birth_date = '1988-10-11'


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker('name')
    slug = factory.Faker('ean', length=8)


class AdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ad

    name = factory.Faker('name')
    price = 18000
    author = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
