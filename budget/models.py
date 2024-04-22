from django.db import models
from django.contrib.auth.models import User

class Wallet(models.Model):
    users = models.ManyToManyField(User, related_name='wallets')
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)

class Category(models.Model):
    name = models.CharField(max_length=255)

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    operation_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(blank=True)

class Revenue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    operation_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
