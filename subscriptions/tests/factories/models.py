import factory
from faker import Faker
from factory.fuzzy import FuzzyChoice, FuzzyDecimal
from subscriptions.models import Customer, Subscription
from datetime import date, timedelta

class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer
    identifier = factory.LazyFunction(lambda: Faker().uuid4())

class SubscriptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subscription

    customer = factory.SubFactory(CustomerFactory)
    start_date = factory.LazyFunction(lambda: Faker().date_between(start_date='2020-01-01', end_date='2020-12-31'))
    end_date = factory.LazyFunction(lambda: date.today() + timedelta(days=30))
    billing_cycle = FuzzyChoice([1, 3, 6, 12])
    price = FuzzyDecimal(3.99, 12.99)