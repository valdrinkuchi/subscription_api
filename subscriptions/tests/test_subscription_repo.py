from django.test import TestCase
from subscriptions.repositories.subscription_repo import SubscriptionRepo
from datetime import date
from subscriptions.tests.factories.models import CustomerFactory, SubscriptionFactory

class SubscriptionRepoTest(TestCase):
    def setUp(self):
        self.customer1 = CustomerFactory.create(name="HD")
        self.customer2 = CustomerFactory.create(name="BMW")

        self.subscription1 = SubscriptionFactory.create(
            customer=self.customer1,
            start_date=date(2022, 1, 1),
            end_date=date(2022, 12, 31),
            billing_cycle=1,
            price=5
        )
        self.subscription2 = SubscriptionFactory.create(
            customer=self.customer1,
            start_date=date(2022, 1, 1),
            end_date=date(2022, 12, 31),
            billing_cycle=1,
            price=10
        )
        self.subscription3 = SubscriptionFactory.create(
            customer=self.customer1,
            start_date=date(2022, 1, 1),
            end_date=date(2022, 12, 31),
            billing_cycle=3,
            price=10
		)
        self.subscription4 = SubscriptionFactory.create(
            customer=self.customer2,
            start_date=date(2022, 1, 1),
            end_date=date(2022, 12, 31),
            billing_cycle=1,
            price=30
        )

        self.subscription_repo = SubscriptionRepo()


    def test_get_accumulated_price_by_month_for_month_1(self):
        customer_id = self.customer1.id
        month = 1
        year = 2022
        expected_accumulated_price = 0
        data = self.subscription_repo.get_accumulated_price_by_month_for(customer_id, month, year)
        self.assertEqual(data['customer'].id, customer_id)
        self.assertEqual(data['subscriptions'].count(), 0)
        self.assertEqual(data['accumulated_price'], expected_accumulated_price)

    def test_get_accumulated_price_by_month_for_month_3(self):
        customer_id = self.customer1.id
        month = 3
        year = 2022
        expected_accumulated_price = 15
        data = self.subscription_repo.get_accumulated_price_by_month_for(customer_id, month, year)
        self.assertEqual(data['customer'].id, customer_id)
        self.assertEqual(data['subscriptions'].count(), 2)
        self.assertEqual(data['accumulated_price'], expected_accumulated_price)

    def test_get_accumulated_price_by_month_for_month_4(self):
        customer_id = self.customer1.id
        month = 4
        year = 2022
        expected_accumulated_price = 25
        data = self.subscription_repo.get_accumulated_price_by_month_for(customer_id, month, year)
        self.assertEqual(data['customer'].id, customer_id)
        self.assertEqual(data['subscriptions'].count(), 3)
        self.assertEqual(data['accumulated_price'], expected_accumulated_price)

    def test_get_all_accumulated_subscription_prices_for_month_1(self):
        month = 1
        year = 2022
        expected_customer_data_count = 1
        data = self.subscription_repo.get_all_accumulated_subscription_prices_for(month, year)
        self.assertEqual(len(data), expected_customer_data_count)
        self.assertEqual(data[0]['customer_name'], None)
        self.assertEqual(data[0]['subscriptions'], [])
        self.assertEqual(data[0]['accumulated_price'], 0)

    def test_get_all_accumulated_subscription_prices_for_month_3(self):
        month = 3
        year = 2022
        expected_customer_data_count = 2
        data = self.subscription_repo.get_all_accumulated_subscription_prices_for(month, year)
        self.assertEqual(len(data), expected_customer_data_count)
        self.assertEqual(data[0]['customer_name'], "HD")
        self.assertEqual(data[0]['subscriptions'].count(), 2)
        self.assertEqual(data[0]['accumulated_price'], 15)
        self.assertEqual(data[1]['customer_name'], "BMW")
        self.assertEqual(data[1]['accumulated_price'], 30)

    def test_get_all_accumulated_subscription_prices_for_month_4(self):
        month = 4
        year = 2022
        expected_customer_data_count = 2
        data = self.subscription_repo.get_all_accumulated_subscription_prices_for(month, year)
        self.assertEqual(len(data), expected_customer_data_count)
        self.assertEqual(data[0]['customer_name'], "HD")
        self.assertEqual(data[0]['subscriptions'].count(), 3)
        self.assertEqual(data[0]['accumulated_price'], 25)
        self.assertEqual(data[1]['customer_name'], "BMW")
        self.assertEqual(data[1]['accumulated_price'], 30)