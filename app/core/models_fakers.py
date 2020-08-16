from .models import AccountType
import factory


class AccountTypeFactory(factory.Factory):
    class Meta:
        model = AccountType
    name = factory.Faker('name')
    icon_name = factory.Faker('color_name')
