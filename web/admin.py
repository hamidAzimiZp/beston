from django.contrib import admin

# Register your models here

from .models import Expense
from .models import Income
from .models import Token
from .models import UserRegister
from .models import Member
from .models import Slider
from .models import News


@admin.register(Token)
class UserTokenAdmin(admin.ModelAdmin):
    pass


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ["text", "user", "amount", "date"]


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ["text", "user", "amount", "date"]


@admin.register(UserRegister)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Member)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    pass

@admin.register(News)
class SliderAdmin(admin.ModelAdmin):
    pass