from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Wallet, Expense, Revenue, Category
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from .forms import ExpenseForm
from .forms import RevenueForm
import matplotlib.pyplot as plt
import io, os
def welcome(request):
    return render(request, 'registration/welcomepage.html')


def home(request):
    return render(request, 'budget/home.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('welcome')

class WalletDetailsView(DetailView):
    model = Wallet
    template_name = 'wallet_details.html'
    context_object_name = 'wallet'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wallet = self.get_object()

        revenues = Revenue.objects.filter(wallet=wallet)
        expenses = Expense.objects.filter(wallet=wallet)

        total_revenue = sum(revenue.amount for revenue in revenues)
        total_expense = sum(expense.amount for expense in expenses)

        context['revenues'] = revenues
        context['expenses'] = expenses
        context['total_revenue'] = total_revenue
        context['total_expense'] = total_expense
        return context
def wallet_chart(request, pk):
    wallet = Wallet.objects.get(pk=pk)
    revenues = Revenue.objects.filter(wallet=wallet)
    expenses = Expense.objects.filter(wallet=wallet)

    total_revenue = sum(revenue.amount for revenue in revenues)
    total_expense = sum(expense.amount for expense in expenses)

    fig, ax = plt.subplots()
    labels = ['Revenues', 'Expenses']
    values = [total_revenue, total_expense]

    ax.bar(labels, values, color=['green', 'red'])
    ax.set_ylabel('Amount', color='white')

    fig.patch.set_facecolor('#1a1a1a')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return HttpResponse(buf, content_type='image/png')
class WalletListView(ListView):
    model = Wallet
    template_name = 'budget/wallet_list.html'


class WalletCreateView(LoginRequiredMixin, CreateView):
    model = Wallet
    fields = ['balance', 'description']
    success_url = reverse_lazy('wallet_list')
    template_name = 'budget/wallet_form.html'

    def form_valid(self, form):
        self.object = form.save()
        self.object.users.add(self.request.user)
        return HttpResponseRedirect(self.get_success_url())


class WalletUpdateView(UpdateView):
    model = Wallet
    fields = ['balance', 'description']
    success_url = reverse_lazy('wallet_list')
    template_name = 'budget/wallet_form.html'


class WalletDeleteView(DeleteView):
    model = Wallet
    success_url = reverse_lazy('wallet_list')
    template_name = 'budget/wallet_confirm_delete.html'


class ExpenseListView(ListView):
    model = Expense
    template_name = 'budget/expense_list.html'


class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    form_class = ExpenseForm
    success_url = reverse_lazy('expenses_list')
    template_name = 'budget/expense_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ExpenseUpdateView(UpdateView):
    model = Expense
    fields = ['user', 'wallet', 'title', 'operation_date', 'amount', 'category', 'description']
    success_url = reverse_lazy('expense_list')
    template_name = 'budget/expense_form.html'


class ExpenseDeleteView(DeleteView):
    model = Expense
    success_url = reverse_lazy('expense_list')
    template_name = 'budget/expense_confirm_delete.html'


class RevenueListView(ListView):
    model = Revenue
    template_name = 'budget/revenue_list.html'


class RevenueCreateView(LoginRequiredMixin, CreateView):
    model = Revenue
    form_class = RevenueForm
    success_url = reverse_lazy('revenues_list')
    template_name = 'budget/revenue_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class RevenueUpdateView(UpdateView):
    model = Revenue
    fields = ['user', 'wallet', 'title', 'operation_date', 'amount', 'category', 'description']
    success_url = reverse_lazy('revenues_list')
    template_name = 'budget/revenue_form.html'


class RevenueDeleteView(DeleteView):
    model = Revenue
    success_url = reverse_lazy('revenue_list')
    template_name = 'budget/revenue_confirm_delete.html'


class CategoryListView(ListView):
    model = Category
    template_name = 'budget/category_list.html'


class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']
    success_url = reverse_lazy('category_list')
    template_name = 'budget/category_form.html'


class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']
    success_url = reverse_lazy('category_list')
    template_name = 'budget/category_form.html'


class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('category_list')
    template_name = 'budget/category_confirm_delete.html'
