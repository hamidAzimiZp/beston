from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, JsonResponse
from json.encoder import JSONEncoder
from django.views.decorators.csrf import csrf_exempt
from .models import User, Token, Income, Expense, UserRegister
from datetime import datetime

from django.core import serializers
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Sum, Count
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.views.decorators.http import require_POST
import random
from django.contrib.auth.decorators import login_required
from .utils import grecaptcha_verify
import string
# from postmark import PMMail

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login

from django.db.models import Sum

def index(request):
    return render(request, "web/index.html")

# create random string for Token
random_str = lambda N: ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(N))


# login , (API) , returns : JSON = statuns (ok|error) and token



def register(request):
    if "requestcode" in request.POST:  # form is filled. if not spam, generate code and save in db, wait for email confirmation, return message
        # is this spam? check reCaptcha
        if not grecaptcha_verify(request):  # captcha was not correct
            context = {
                'message': 'کپچای گوگل درست وارد نشده بود. شاید ربات هستید؟ کد یا کلیک یا تشخیص عکس زیر فرم را درست پر کنید. ببخشید که فرم به شکل اولیه برنگشته!'}  # TODO: forgot password
            return render(request, 'registration/register.html', context)

        # duplicate email
        if User.objects.filter(email=request.POST['email']).exists():
            context = {
                'message': 'متاسفانه این ایمیل قبلا استفاده شده است. در صورتی که این ایمیل شما است، از صفحه ورود گزینه فراموشی پسورد رو انتخاب کنین. ببخشید که فرم ذخیره نشده. درست می شه'}  # TODO: forgot password
            # TODO: keep the form data
            return render(request, 'registration/register.html', context)
        # if user does not exists
        if not User.objects.filter(username=request.POST['username']).exists():
            code = get_random_string(length=32)
            now = datetime.now()
            email = request.POST['email']
            password = make_password(request.POST['password'])
            username = request.POST['username']
            temporarycode = UserRegister(
                email=email, time=now, code=code, username=username, password=password)
            temporarycode.save()
            # message = PMMail(api_key=settings.POSTMARK_API_TOKEN,
            #                 subject="فعالسازی اکانت بستون",
            #                 sender="hamidazimi44100@gmail.com",
            #                 to=email,
            #                 text_body=" برای فعال کردن اکانت بستون خود روی لینک روبرو کلیک کنید: {}?code={}".format(
            #                     request.build_absolute_uri('/register/'), code),
            #                 tag="account request")
            # message.send()
            # message = 'ایمیلی حاوی لینک فعال سازی اکانت به شما فرستاده شده، لطفا پس از چک کردن ایمیل، روی لینک کلیک کنید.'
            message = 'قدیم ها ایمیل فعال سازی می فرستادیم ولی الان شرکتش ما رو تحریم کرده (: پس راحت و بی دردسر'
            body = " برای فعال کردن اکانت بستون خود روی لینک روبرو کلیک کنید: \n<a href=\"{0}?code={1}\">\"{0}?code={1}\"</a>".format(request.build_absolute_uri('/register/'), code)
            message = message + body
            context = {
                'message': message 
                }
            return render(request, 'registration/register.html', context)
        
        else:
            context = {
                'message': 'متاسفانه این نام کاربری قبلا استفاده شده است. از نام کاربری دیگری استفاده کنید. ببخشید که فرم ذخیره نشده. درست می شه'}  # TODO: forgot password
            # TODO: keep the form data
            return render(request, 'registration/register.html', context)
    elif "code" in request.GET:  # user clicked on code
        code = request.GET['code']
        if UserRegister.objects.filter(code=code).exists():  # if code is in temporary db, read the data and create the user
            new_temp_user = UserRegister.objects.get(code=code)
            newuser = User.objects.create(username=new_temp_user.username, password=new_temp_user.password,
                                          email=new_temp_user.email)
            this_token = get_random_string(length=48)
            token = Token.objects.create(user=newuser, token=this_token)
            # delete the temporary activation code from db
            UserRegister.objects.filter(code=code).delete()
            context = {
                'message': 'اکانت شما ساخته شد. توکن شما {} است. آن را ذخیره کنید چون دیگر نمایش داده نخواهد شد! جدی!'.format(
                    this_token)}
            return render(request, 'registration/register.html', context)
        else:
            context = {
                'message': 'این کد فعال سازی معتبر نیست. در صورت نیاز دوباره تلاش کنید'}
            return render(request, 'registration/register.html', context)
    else:
        context = {'message': ''}
        return render(request, 'registration/register.html', context)


def login(request):
    
    if "requestcode" in request.POST:  # form is filled. if not spam, generate code and save in db, wait for email confirmation, return message
        # is this spam? check reCaptcha
        if not grecaptcha_verify(request):  # captcha was not correct
            context = {
                'message': 'کپچای گوگل درست وارد نشده بود. شاید ربات هستید؟ کد یا کلیک یا تشخیص عکس زیر فرم را درست پر کنید. ببخشید که فرم به شکل اولیه برنگشته!'}  # TODO: forgot password
            return render(request, 'registration/login.html', context)    
            
        if "username" in request.POST and "password" in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth_login(request, user)
                
                return redirect('/account/dashboard/')
                    
            else:
                context = {
                    "message" : "نام کاربری یا پسورد نادرست وارد شده است"
                }
                
                return render(request, "registration/login.html", context)
            
    else:
        context = {'message': ''}
        return render(request, 'registration/login.html', context)
        
    
@csrf_exempt    
def submit_expense(request):
    """ submit an expone """
    
    # send from curl
    # curl --data "token=1234567&text=ghelian&amount=5000" http://localhost:8000/submit/expense/
    
    # get token
    this_token = request.POST["token"]
    
    # get user with token
    this_user = User.objects.filter(token__token = this_token).get()
    
    # get amount
    this_amount = request.POST["amount"]
    
    # get text
    this_text = request.POST["text"]
    
    # get time
    if not "date" in request.POST:
        this_date = datetime.now() 
    else:
        this_date = request.POST["date"]

    Expense.objects.create(user = this_user, 
                           amount = this_amount, 
                           text = this_text,
                           date = this_date,)
    
    print("I'm submit expense")
    print(request.POST)
    
    
    return JsonResponse({
       "status" : "ok"
    }, encoder = JSONEncoder)
    
    
@csrf_exempt    
def submit_income(request):
    """ submit an income """
    # send from curl
    # curl --data "token=1234567&text=ghelian&amount=5000" http://localhost:8000/submit/expense/
    
    # get token
    this_token = request.POST["token"]
    
    # get user with token
    this_user = User.objects.filter(token__token = this_token).get()
    
    # get amount
    this_amount = request.POST["amount"]
    
    # get text
    this_text = request.POST["text"]
    
    # get time
    if not "date" in request.POST:
        this_date = datetime.now() 
    else:
        this_date = request.POST["date"]

    Income.objects.create(user = this_user, 
                           amount = this_amount, 
                           text = this_text,
                           date = this_date,)
    
    print("I'm submit expense")
    print(request.POST)
    
    
    return JsonResponse({
       "status" : "ok"
    }, encoder = JSONEncoder)



def user_status(request):
    
    this_user = request.user
    now = datetime.now()
        
    income_count = Income.objects.filter(user__username = this_user).all().count()
    income_field = Income.objects.filter(user__username = this_user)
    total_income_dict = Income.objects.filter(user=this_user).aggregate(Sum("amount"))
    for key, value in total_income_dict.items():
        total_income = value
    
    
    expense_count = Expense.objects.filter(user__username = this_user).all().count()
    expense_field = Expense.objects.filter(user__username = this_user)
    total_expense_dict = Expense.objects.filter(user=this_user).aggregate(Sum("amount"))
    for key, value in total_expense_dict.items():
        total_expense = value
        
    context = {
        "income_count" : income_count,
        "income_field" : income_field,  
        "expense_count" : expense_count,
        "expense_field" : expense_field,
        "now" : now,
        "total_income" : total_income,
        "total_expense" : total_expense,
    }
    
    return render(request, "web/dashboard_status.html", context)
    
    
    
@login_required
def dashboard(request):
    this_user = request.user
    now = datetime.now()
    
    
    def setExpese():
        if "text" in request.POST and "amount" in request.POST :
            
            this_text = request.POST["text"]
            this_amount = request.POST["amount"]
                
            if not "date" in request.POST:
                this_date = datetime.now()
            else:
                this_date = request.POST["date"]
            
            post_content = Expense(user = this_user, text = this_text, amount = this_amount,
                                    date=this_date)
            post_content.save()
    
    
    def setIncome():
        if "text" in request.POST and "amount" in request.POST :
            
            this_text = request.POST["text"]
            this_amount = request.POST["amount"]
                
            if not "date" in request.POST:
                this_date = datetime.now()
            else:
                this_date = request.POST["date"]
            
            post_content = Income(user = this_user, text = this_text, amount = this_amount,
                                    date=this_date)
            post_content.save()
    
    
    if "expense" in request.POST:
        setExpese()
        
    elif "income" in request.POST:
        setIncome()
        
        
    context = {
        "now" : now
    }
    return render(request, "web/dashboard.html", context)