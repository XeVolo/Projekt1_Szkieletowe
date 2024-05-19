from django.contrib import admin
from .models import Wallet, Category, Expense, Revenue


# Define custom admin classes for each model


class WalletAdmin(admin.ModelAdmin):
    list_display = ('description', 'balance')
    filter_horizontal = ('users',)



class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)



class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'wallet', 'operation_date', 'amount', 'category')
    list_filter = ('user', 'wallet', 'category')
    search_fields = ('title', 'description')



class RevenueAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'wallet', 'operation_date', 'amount', 'category')
    list_filter = ('user', 'wallet', 'category')
    search_fields = ('title', 'description')


# Register the custom admin classes with the admin site

admin.site.register(Wallet, WalletAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Revenue, RevenueAdmin)
