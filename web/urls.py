from django.urls import path, re_path

from . import views
from django.views.generic import RedirectView



app_name = "web"
urlpatterns = [
    path("", views.index, name = "index"),
    re_path(r"^submit/expense/$", views.submit_expense, name = "submitExpense"),
    re_path(r"^submit/income/$", views.submit_income, name = "submitIncome"),
    path("register/", views.register, name = "register"),
    path('login/', views.login, name='login'),
    path("account/dashboard/", views.dashboard, name = "dashboard"),
    path("account/dashboard/status", views.user_status, name = "userStatus"),
    path("favicon\.ico/", RedirectView.as_view(url='/static/_images/favicon.ico'))
]