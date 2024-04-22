from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # Widoki dla modelu Wallet
    path('wallet/', views.WalletListView.as_view(), name='wallet_list'),
    path('wallet/create/', views.WalletCreateView.as_view(), name='wallet_create'),
    path('wallet/<int:pk>/update/', views.WalletUpdateView.as_view(), name='wallet_update'),
    path('wallet/<int:pk>/delete/', views.WalletDeleteView.as_view(), name='wallet_delete'),

    # Widoki dla modelu Expenses
    path('expenses/', views.ExpenseListView.as_view(), name='expenses_list'),
    path('expenses/create/', views.ExpenseCreateView.as_view(), name='expenses_create'),
    path('expenses/<int:pk>/update/', views.ExpenseUpdateView.as_view(), name='expenses_update'),
    path('expenses/<int:pk>/delete/', views.ExpenseDeleteView.as_view(), name='expenses_delete'),

    # Widoki dla modelu Revenues
    path('revenues/', views.RevenueListView.as_view(), name='revenues_list'),
    path('revenues/create/', views.RevenueCreateView.as_view(), name='revenues_create'),
    path('revenues/<int:pk>/update/', views.RevenueUpdateView.as_view(), name='revenues_update'),
    path('revenues/<int:pk>/delete/', views.RevenueDeleteView.as_view(), name='revenues_delete'),

    # Widoki dla modelu Category
    path('category/', views.CategoryListView.as_view(), name='category_list'),
    path('category/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('category/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('category/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),

    # Widoki rejestracji i logowania
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
