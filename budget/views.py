from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Wallet, Expense, Revenue, Category
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Przekierowanie po rejestracji
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Przekierowanie po zalogowaniu
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')  # Przekierowanie po wylogowaniu


class WalletListView(ListView):
    model = Wallet
    template_name = 'wallet_list.html'

class WalletCreateView(CreateView):
    model = Wallet
    fields = ['balance', 'description']
    success_url = reverse_lazy('wallet_list')
    template_name = 'wallet_form.html'

class WalletUpdateView(UpdateView):
    model = Wallet
    fields = ['balance', 'description']
    success_url = reverse_lazy('wallet_list')
    template_name = 'wallet_form.html'

class WalletDeleteView(DeleteView):
    model = Wallet
    success_url = reverse_lazy('wallet_list')
    template_name = 'wallet_confirm_delete.html'


class ExpenseListView(ListView):
    model = Expense
    template_name = 'expense_list.html'

class ExpenseCreateView(CreateView):
    model = Expense
    fields = ['user', 'wallet', 'title', 'operation_date', 'amount', 'category', 'description']
    success_url = reverse_lazy('expenses_list')
    template_name = 'expense_form.html'

class ExpenseUpdateView(UpdateView):
    model = Expense
    fields = ['user', 'wallet', 'title', 'operation_date', 'amount', 'category', 'description']
    success_url = reverse_lazy('expense_list')
    template_name = 'expense_form.html'

class ExpenseDeleteView(DeleteView):
    model = Expense
    success_url = reverse_lazy('expense_list')
    template_name = 'expense_confirm_delete.html'


class RevenueListView(ListView):
    model = Revenue
    template_name = 'revenue_list.html'

class RevenueCreateView(CreateView):
    model = Revenue
    fields = ['user', 'wallet', 'title', 'operation_date', 'amount', 'category', 'description']
    success_url = reverse_lazy('revenue_list')
    template_name = 'revenue_form.html'

class RevenueUpdateView(UpdateView):
    model = Revenue
    fields = ['user', 'wallet', 'title', 'operation_date', 'amount', 'category', 'description']
    success_url = reverse_lazy('revenues_list')
    template_name = 'revenue_form.html'

class RevenueDeleteView(DeleteView):
    model = Revenue
    success_url = reverse_lazy('revenue_list')
    template_name = 'revenue_confirm_delete.html'

class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'

class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']
    success_url = reverse_lazy('category_list')
    template_name = 'category_form.html'

class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']
    success_url = reverse_lazy('category_list')
    template_name = 'category_form.html'

class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('category_list')
    template_name = 'category_confirm_delete.html'
