from django import forms
from .models import Expense, Category


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['wallet', 'title', 'operation_date', 'amount', 'category', 'description']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ExpenseForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['wallet'].queryset = user.wallets.all()
            self.fields['wallet'].empty_label = None
            self.fields['wallet'].label_from_instance = lambda obj: obj.description

            self.fields['category'].widget = forms.Select(choices=[(category.name, category.name) for category in Category.objects.all()])

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Subtract the amount from the selected wallet's balance only if the instance is not saved yet
        if not instance.pk:
            instance.wallet.balance -= instance.amount

        if commit:
            instance.wallet.save()  # Save the updated wallet balance
            instance.save()  # Save the expense
        return instance
