from django.contrib import admin

# Register your models here

from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    pass
