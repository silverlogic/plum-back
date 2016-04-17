from datetime import date

import factory


class UserFactory(factory.DjangoModelFactory):
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'default')

    class Meta:
        model = 'users.User'


class FamilyFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'family.Family'


class ParentFactory(factory.DjangoModelFactory):
    family = factory.SubFactory('tests.factories.FamilyFactory')
    user = factory.SubFactory('tests.factories.UserFactory')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

    class Meta:
        model = 'family.Parent'


class KidFactory(factory.DjangoModelFactory):
    family = factory.SubFactory('tests.factories.FamilyFactory')
    name = factory.Faker('name')

    class Meta:
        model = 'family.Kid'


class CardFactory(factory.DjangoModelFactory):
    family = factory.SubFactory('tests.factories.FamilyFactory')
    owner = factory.SubFactory('tests.factories.ParentFactory')
    name_on_card = 'John Smalls'
    number = '4895142232120006'
    expiration_date = date(2018, 7, 1)
    type = 'C'
    sub_type = ''

    class Meta:
        model = 'cards.Card'
