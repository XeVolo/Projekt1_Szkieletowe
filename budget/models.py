from django.db import models

from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone_number = models.IntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=100)

class Wallet(models.Model):
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True, null=True)

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    operation_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True, null=True)

class Revenue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    operation_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True, null=True)

class Category(models.Model):
    name = models.CharField(max_length=100)


