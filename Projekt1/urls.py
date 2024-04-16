from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("budget/", include("budget.urls")),
    path("admin/", admin.site.urls),
]
