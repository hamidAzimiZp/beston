from django.urls import path, re_path

from . import views



app_name = "web"
urlpatterns = [
    re_path(r"^submit/expense/$", views.submit_expense, name = "submitExpense"),
    re_path(r"^submit/income/$", views.submit_income, name = "submitIncome"),
]