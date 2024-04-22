from django.contrib import admin
from .models import Wallet, Expense, Revenue, Category

admin.site.register(Wallet)
admin.site.register(Expense)
admin.site.register(Revenue)
admin.site.register(Category)