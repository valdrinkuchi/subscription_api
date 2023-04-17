from subscriptions.models import Customer, Subscription
from django.db.models import Sum
from django.db.models import Q
from datetime import date
from dateutil.relativedelta import relativedelta

class SubscriptionRepo:
    """
	This repo is responsible for all db fetches that are neccessary with regards
    to the subscriptions. In a way this is the only place which is reponible for
    making queries using the ORM. If we wanted to change the db and the query
    library this is the ony place we would need to adjust/change.
	"""

    def get_accumulated_price_by_month_for(self, customer_id, month, year):
        """
        Gets the accumulated price for all subscriptions of a customer that should
        be billed during the provided month. Ideally we would exclude the already
        billed subscriptions.
        If subscriptions are a long array we could refrain from returning all of
        them. We could put a limit.
        """
        subscriptions = self._get_subscriptions_by_month_year(month, year, customer_id = customer_id)
        accumulated_price = subscriptions.aggregate(Sum('price'))['price__sum']
        accumulated_price = accumulated_price or 0
        data = {
            'customer': Customer.objects.get(id=customer_id),
            'subscriptions': subscriptions,
            'accumulated_price': accumulated_price
            }
        return data

    def get_all_accumulated_subscription_prices_for(self, month, year):
        """
        Gets the accumulated price for all subscriptions for all customers. It
        also includes the total price amount for each customer.
        """
        customer_accumulated_prices = {}
        customers = Customer.objects.all()
        subscriptions = self._get_subscriptions_by_month_year(month, year)
        if subscriptions:
            for subscription in subscriptions:
                customer_id = subscription.customer_id
                accumulated_price = self._calculate_customer_accumulated_price([subscription])
                customer_accumulated_prices[customer_id] = customer_accumulated_prices.get(customer_id, 0) + accumulated_price
            customer_data = []
            for customer in customers:
                if not subscriptions.filter(customer_id=customer.id):
                    continue
                customer_data.append({
                    'customer_name': customer.name,
                    'id': customer.id,
                    'subscriptions': subscriptions.filter(customer_id=customer.id),
                    'accumulated_price': customer_accumulated_prices.get(customer.id, 0)
                })

            return customer_data
        return [
                {
                    'customer_name': None,
                    'id': None,
                    'subscriptions': [],
                    'accumulated_price': 0
                }
            ]

    def _get_subscriptions_by_month_year(self, month, year, customer_id=None):
        date_to_compare = date(year, month, 1)
        query = Q(end_date__gt=date_to_compare)
        if customer_id:
            query &= Q(customer_id=customer_id)
        subscriptions = Subscription.objects.filter(query)
        for subscription in subscriptions:
            billing_dates = self._calculate_billing_dates(subscription.start_date, subscription.billing_cycle)
            if date_to_compare not in billing_dates:
                subscriptions = subscriptions.exclude(id=subscription.id)
        return subscriptions

    def _calculate_billing_dates(self, start_date, billing_cycle):
        billing_dates = []
        billing_date = start_date

        for _ in range(12):
            billing_date += relativedelta(months=billing_cycle)
            billing_dates.append(billing_date)
        return billing_dates

    def _calculate_customer_accumulated_price(self, subscriptions):
        accumulated_price = sum(subscription.price for subscription in subscriptions)
        return accumulated_price
