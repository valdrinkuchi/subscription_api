from django.core.management.base import BaseCommand
from faker import Faker
from decimal import Decimal
from datetime import datetime
from subscriptions.models import Customer, Subscription

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        fake = Faker()

        for _ in range(3):
            customer = Customer.objects.create(
                name=fake.name(),
                identifier=fake.uuid4()
            )

            for _ in range(10):
                Subscription.objects.create(
                    customer=customer,
                    price=Decimal('12.99'),
                    billing_cycle=1,
                    start_date=datetime(2023, 1, 1),
                    end_date=datetime(2023, 12, 31),
                )

            for _ in range(15):
                Subscription.objects.create(
                    customer=customer,
                    price=Decimal('7.99'),
                    billing_cycle=3,
                    start_date=datetime(2023, 1, 1),
                    end_date=datetime(2023, 12, 31),
                )