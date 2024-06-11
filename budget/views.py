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
from django.shortcuts import get_object_or_404
import datetime
import matplotlib.dates as mdates


#strona powitalna
def welcome(request):
    return render(request, 'registration/welcomepage.html')

#główny widok aplikacji
def home(request):
    return render(request, 'budget/home.html')

#rejestracja
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

#logowanie
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

#wylogowywanie
def user_logout(request):
    logout(request)
    return redirect('welcome')

#Widok portfela
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

#generowanie wykresu słupkowego
def wallet_bar_chart(request, pk):
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

#generowanie wykresu liniowego
def wallet_line_chart(request, pk):
    wallet = get_object_or_404(Wallet, pk=pk)
    revenues = Revenue.objects.filter(wallet=wallet).order_by('operation_date')
    expenses = Expense.objects.filter(wallet=wallet).order_by('operation_date')

    revenue_dates = [revenue.operation_date.strftime('%d-%m-%Y') for revenue in revenues]
    revenue_amounts = [revenue.amount for revenue in revenues]

    expense_dates = [expense.operation_date.strftime('%d-%m-%Y') for expense in expenses]
    expense_amounts = [expense.amount for expense in expenses]

    combined_data = []
    for revenue in revenues:
        revenue_date_formatted = revenue.operation_date.strftime('%d-%m-%Y')
        combined_data.append({
            "amount": revenue.amount,
            "date": revenue_date_formatted,
            "type": 0
        })

    for expense in expenses:
        expense_date_formatted = expense.operation_date.strftime('%d-%m-%Y')
        combined_data.append({
            "amount": expense.amount,
            "date": expense_date_formatted,
            "type": 1
        })

    for item in combined_data:
        item["date"] = datetime.datetime.strptime(item["date"], '%d-%m-%Y')

    sorted_data = sorted(combined_data, key=lambda x: x["date"])

    fig2, ax2 = plt.subplots()

    types = [item["type"] for item in sorted_data]
    revenue_indices = [i for i, t in enumerate(types) if t == 0]
    expense_indices = [i for i, t in enumerate(types) if t == 1]

    revenue_dates = [sorted_data[i]["date"] for i in revenue_indices]
    revenue_amounts = [sorted_data[i]["amount"] for i in revenue_indices]
    expense_dates = [sorted_data[i]["date"] for i in expense_indices]
    expense_amounts = [sorted_data[i]["amount"] for i in expense_indices]

    ax2.plot(expense_dates, expense_amounts, label='Expenses', color='red')
    ax2.scatter(expense_dates, expense_amounts, label='Expenses', color='red')
    ax2.plot(revenue_dates, revenue_amounts, label='Revenues', color='green')
    ax2.scatter(revenue_dates, revenue_amounts, label='Revenues', color='green')

    ax2.set_xlabel('Date', color='white')
    ax2.set_ylabel('Amount', color='white')

    ax2.legend(facecolor='#1a1a1a', edgecolor='white', labelcolor='white')

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
    plt.gcf().autofmt_xdate()
    fig2.patch.set_facecolor('#1a1a1a')
    ax2.xaxis.label.set_color('white')
    ax2.yaxis.label.set_color('white')
    ax2.tick_params(axis='x', colors='white')
    ax2.tick_params(axis='y', colors='white')
    ax2.set_ylim(bottom=0)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return HttpResponse(buf, content_type='image/png')

#Widok listy portfeli
class WalletListView(LoginRequiredMixin, ListView):
    model = Wallet
    template_name = 'budget/wallet_list.html'
    context_object_name = 'wallets'

    def get_ordering(self):
        ordering = self.request.GET.get('ordering', 'description')
        direction = self.request.GET.get('direction', 'asc')
        if direction == 'desc':
            ordering = f'-{ordering}'
        return ordering

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(users=self.request.user)  # Filtruj portfele tylko dla zalogowanego użytkownika
        ordering = self.get_ordering()
        if ordering:
            queryset = queryset.order_by(ordering)
        return queryset


#tworzenie nowego portfela
class WalletCreateView(LoginRequiredMixin, CreateView):
    model = Wallet
    fields = ['balance', 'description']
    success_url = reverse_lazy('wallet_list')
    template_name = 'budget/wallet_form.html'

    def form_valid(self, form):
        self.object = form.save()
        self.object.users.add(self.request.user)
        return HttpResponseRedirect(self.get_success_url())


#Edytowanie portfela
class WalletUpdateView(UpdateView):
    model = Wallet
    fields = ['balance', 'description']
    success_url = reverse_lazy('wallet_list')
    template_name = 'budget/wallet_form.html'

#Usuwanie portfela
class WalletDeleteView(DeleteView):
    model = Wallet
    success_url = reverse_lazy('wallet_list')
    template_name = 'budget/wallet_confirm_delete.html'

#Tworzenie wydatków - lista
class ExpenseListView(ListView):
    model = Expense
    template_name = 'budget/expense_list.html'
    context_object_name = 'expenses'

    def get_ordering(self):
        ordering = self.request.GET.get('ordering', 'title')
        direction = self.request.GET.get('direction', 'asc')
        if direction == 'desc':
            ordering = f'-{ordering}'
        return ordering

    def get_queryset(self):
        queryset = super().get_queryset()
        ordering = self.get_ordering()
        if ordering:
            queryset = queryset.order_by(ordering)
        queryset = queryset.filter(user=self.request.user)
        return queryset


#Widok tworzenia wydatków
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

#Edytowanie wydatków
class ExpenseUpdateView(UpdateView):
    model = Expense
    fields = ['user', 'wallet', 'title', 'operation_date', 'amount', 'category', 'description']
    success_url = reverse_lazy('expense_list')
    template_name = 'budget/expense_form.html'

#Usuwanie wydatków
class ExpenseDeleteView(DeleteView):
    model = Expense
    success_url = reverse_lazy('expense_list')
    template_name = 'budget/expense_confirm_delete.html'

#Widok przychodów - lista
class RevenueListView(ListView):
    model = Revenue
    template_name = 'budget/revenue_list.html'
    context_object_name = 'revenues'

    def get_ordering(self):
        ordering = self.request.GET.get('ordering', 'title')
        direction = self.request.GET.get('direction', 'asc')
        if direction == 'desc':
            ordering = f'-{ordering}'
        return ordering

    def get_queryset(self):
        queryset = super().get_queryset()
        ordering = self.get_ordering()
        if ordering:
            queryset = queryset.order_by(ordering)
        queryset = queryset.filter(user=self.request.user)
        return queryset

#Widok dodawnia przychodów
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

#Edytowanie dodanych przychodów
class RevenueUpdateView(UpdateView):
    model = Revenue
    fields = ['user', 'wallet', 'title', 'operation_date', 'amount', 'category', 'description']
    success_url = reverse_lazy('revenues_list')
    template_name = 'budget/revenue_form.html'

#Usuwanie przychodów
class RevenueDeleteView(DeleteView):
    model = Revenue
    success_url = reverse_lazy('revenue_list')
    template_name = 'budget/revenue_confirm_delete.html'

#Lista dodanych kategorii
class CategoryListView(ListView):
    model = Category
    template_name = 'budget/category_list.html'
    context_object_name = 'categories'

    def get_ordering(self):
        ordering = self.request.GET.get('ordering', 'name')
        direction = self.request.GET.get('direction', 'asc')
        if direction == 'desc':
            ordering = f'-{ordering}'
        return ordering

    def get_queryset(self):
        queryset = super().get_queryset()
        ordering = self.get_ordering()
        if ordering:
            queryset = queryset.order_by(ordering)
        return queryset

#widok do tworzenia nowych kategorii
class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']
    success_url = reverse_lazy('category_list')
    template_name = 'budget/category_form.html'

#Widok edytowania kategorii
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']
    success_url = reverse_lazy('category_list')
    template_name = 'budget/category_form.html'

#Usuwanie kategorii
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('category_list')
    template_name = 'budget/category_confirm_delete.html'
