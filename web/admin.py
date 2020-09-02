from django.contrib import admin

# Register your models here

from .models import Expense
from .models import Income
from .models import Token
from .models import userRegister

@admin.register(Token)
class UserTokenAdmin(admin.ModelAdmin):
    pass


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ["text", "user", "amount", "date"]


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ["text", "user", "amount", "date"]


@admin.register(userRegister)
class UserAdmin(admin.ModelAdmin):
    pass
