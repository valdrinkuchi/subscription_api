from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=255)
    identifier = models.CharField(max_length=255)

class Subscription(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    billing_cycle = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()