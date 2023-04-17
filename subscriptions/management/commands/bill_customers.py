from django.core.management.base import BaseCommand
import datetime
from subscriptions.repositories.subscription_repo import SubscriptionRepo
from subscriptions.services.billing.billing_service import BillingService

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        repository = SubscriptionRepo()
        service = BillingService()
        month = datetime.datetime.now().month
        year = datetime.datetime.now().year
        customers = repository.get_all_accumulated_subscription_prices_for(month, year)
        for customer in customers:
            for subscription in customer['subscriptions']:
              service.call(subscription)
