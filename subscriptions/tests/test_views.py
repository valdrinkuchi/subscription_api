from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from datetime import date
from rest_framework.test import APIClient
from subscriptions.tests.factories.models import CustomerFactory, SubscriptionFactory
from subscriptions.serializers import SubscriptionSerializer, SubscriptionPriceSerializer, CustomerDataSerializer, CustomerSerializer
from subscriptions.models import *
from faker import Faker

class ViewTests(TestCase):
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

        self.client = APIClient()
        self.fake = Faker()

    def test_customer_create_view(self):
        url = reverse('customer-list')
        data = {'name': 'HD-NEW', 'identifier' : self.fake.uuid4()}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 3)
        expected_data = CustomerSerializer(Customer.objects.filter(name='HD-NEW').first(), many=False).data
        self.assertEqual(response.data, expected_data)

    def test_customer_update_view(self):
        customer = CustomerFactory.create(name="HD-UPDATE")
        url = reverse('customer-detail', args=[customer.id])
        data = {'name': 'HD-UPDATED', 'identifier': self.fake.uuid4()}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        customer.refresh_from_db()
        self.assertEqual(customer.name, 'HD-UPDATED')

    def test_customer_delete_view(self):
        customer = CustomerFactory.create(name="HD-DELETE")
        url = reverse('customer-detail', args=[customer.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Customer.objects.filter(id=customer.id).exists())

    def test_subscription_create_view(self):
        url = reverse('subscription-list')
        data = {
            'customer': self.customer1.id,
            'start_date': date(2022,1,1),
            'end_date': date(2022,12,31),
            'billing_cycle': 1,
            'price': 5
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.count(), 5)
        expected_data = SubscriptionSerializer(Subscription.objects.filter(customer=self.customer1).last(), many=False).data
        self.assertEqual(response.data, expected_data)

    def test_subscription_update_view(self):
        url = reverse('subscription-detail', args=[self.subscription1.id])
        data = {
            'customer': self.subscription1.customer.id,
            'start_date': self.subscription1.start_date,
            'end_date': self.subscription1.end_date,
            'billing_cycle': 3,
            'price': 15
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.subscription1.refresh_from_db()
        self.assertEqual(self.subscription1.billing_cycle, 3)
        self.assertEqual(self.subscription1.price, 15)

    def test_subscription_delete_view(self):
        url = reverse('subscription-detail', args=[self.subscription1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Subscription.DoesNotExist):
            self.subscription1.refresh_from_db()

    def test_accumulated_price_view(self):
        url = reverse('accumulated_price', kwargs={'customer_id': 1})
        response = self.client.get(url, {'month': 4, 'year': 2022})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = {
            'customer': self.customer1,
            'subscriptions': [self.subscription1, self.subscription2, self.subscription3],
            'accumulated_price': 25
          }
        serializer = SubscriptionPriceSerializer(data)
        self.assertEqual(response.data, serializer.data)

    def test_accumulated_prices_list_view(self):
        url = reverse('accumulated_prices_list')
        response = self.client.get(url, {'month': 4, 'year': 2022})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        data = [{
                  'customer_name': self.customer1.name,
                  'id': self.customer1.id,
                  'subscriptions': [self.subscription1, self.subscription2, self.subscription3],
                  'accumulated_price': 25
                },
                {
                  'customer_name': self.customer2.name,
                  'id': self.customer2.id,
                  'subscriptions': [self.subscription4],
                  'accumulated_price': 30
                }]
        serializer = CustomerDataSerializer(data, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_accumulated_price_view(self):
        url = reverse('accumulated_price', kwargs={'customer_id': 1})
        response = self.client.get(url, {'year': 2022})

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data, {'error': 'month query parameter is missing'})

    def test_accumulated_prices_list_view(self):
        url = reverse('accumulated_prices_list')
        response = self.client.get(url, {'year': 2022})

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data, {'error': 'month query parameter is missing'})
