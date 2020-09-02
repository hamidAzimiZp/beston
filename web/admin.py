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
    pass


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    pass


@admin.register(userRegister)
class UserAdmin(admin.ModelAdmin):
    pass
