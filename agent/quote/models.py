from django.db import models


class Customer(models.Model):
    """
        Model for Customer Attributes
    """
    agent = models.ForeignKey('Agent')
    name = models.CharField(max_length=128)

    HOMEOWNER = 'hom'
    OTHER = 'oth'

    TYPE_CHOICES = (
        (HOMEOWNER, 'Homeowner'),
        (OTHER, 'Other'),
    )
    customer_type = models.CharField(
        max_length=3,
        choices=TYPE_CHOICES,
        default=HOMEOWNER,
    )


class Quote(models.Model):
    """
        Model for Quote Attributes
    """
    customer = models.ForeignKey('Customer')
    address = models.CharField(max_length=128)
    new_quote = models.BooleanField(default=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    date = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)


class Agent(models.Model):
    """
        Model for Agent Attributes
    """
    name = models.CharField(max_length=128)
