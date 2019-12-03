from django.db import models
from django.contrib.auth.models import User, AbstractUser
from users.models import MainUser, Profile
from .constants import ORDER_DONE, ORDER_ACTIVE,ORDER_WAITING, ORDER_STATUSES


class Person(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    class Meta:
        abstract = True


class City(models.Model):
    name = models.CharField(max_length=100)
    audcompanies = models.CharField(max_length=100)
    revcompanies = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class AudCompany(models.Model):
    name = models.CharField(max_length=100)
    city_id = models.ForeignKey('City', on_delete=models.CASCADE)
    auditor_id = models.ForeignKey('Auditor', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}:{self.auditor_id}'


class Auditor(Person):

    email = models.EmailField()
    company_id = models.ForeignKey('AudCompany', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}: {self.name}'


class ReviewedCompany(models.Model):
    rating = models.IntegerField()
    name = models.CharField(max_length=100)
    city_id = models.ForeignKey('City', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class OrderDoneManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=ORDER_DONE)

    def done_orders(self):
        return self.filter(status=ORDER_DONE)

    def filter_by_status(self, status):
        return self.filter(status=status)


class OrderWaitingManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=ORDER_WAITING)

    def done_orders(self):
        return self.filter(status=ORDER_DONE)

    def filter_by_status(self, status):
        return self.filter(status=status)

class OrderActiveManager(models.Model):
    def get_queryset(self):
        return super().get_queryset().filter(status=ORDER_ACTIVE)



class Order(models.Model):
    name = models.CharField(max_length=100)
    company_id = models.ForeignKey('ReviewedCompany', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    body = models.TextField()
    status = models.PositiveSmallIntegerField(choices=ORDER_STATUSES, default=ORDER_WAITING)
    company_id = models.ForeignKey('ReviewedCompany', on_delete=models.CASCADE)
    auditor_id = models.ForeignKey('Auditor', on_delete=models.CASCADE)
    order_id = models.ForeignKey('Order', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('users.MainUser', on_delete=models.DO_NOTHING, related_name='creator_reviews')

    objects = models.Manager()
    done_orders = OrderDoneManager()
    waiting_orders = OrderWaitingManager()
    active_orders = OrderActiveManager()

    def __str__(self):
        return f'{self.company_id}:{self.title}'



# Create your models here.
