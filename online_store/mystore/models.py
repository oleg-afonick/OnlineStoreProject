from django.core.validators import MinValueValidator
from django.db import models
from datetime import datetime, timezone
from django.contrib.auth.models import User
from django.urls import reverse


# from .resources import POSITIONS


class Staff(models.Model):
    director = 'DI'
    admin = 'AD'
    cook = 'CO'
    cashier = 'CA'
    cleaner = 'CL'

    POSITIONS = [
        (director, 'Директор'),
        (admin, 'Администратор'),
        (cook, 'Повар'),
        (cashier, 'Кассир'),
        (cleaner, 'Уборщик'),
    ]

    full_name = models.CharField(max_length=255)
    position = models.CharField(choices=POSITIONS, max_length=2, default='DI')
    labor_contract = models.IntegerField()


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.0, validators=[MinValueValidator(0)])
    description = models.CharField(max_length=255, default='description')

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])


class Order(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(null=True, blank=True)
    cost = models.FloatField(default=0.0)
    pickup = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='ProductOrder')

    def __str__(self):
        return f'Заказ #{self.pk}'

    def finish_order(self):
        self.time_out = datetime.now(timezone.utc)
        self.complete = True
        self.save()

    def get_duration(self):
        if self.complete:
            return (self.time_out - self.time_in).total_seconds()
        else:
            return (datetime.now(timezone.utc) - self.time_in).total_seconds()


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    _amount = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.order}: {self.product.price}'

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = int(value) if value >= 0 else 0
        self.save()

    def product_sum(self):
        product_price = self.product.price
        return product_price * self._amount


class Author(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
