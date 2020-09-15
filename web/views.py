from django.shortcuts import redirect, render, get_list_or_404
from django.http import JsonResponse
from json.encoder import JSONEncoder
from django.views.decorators.csrf import csrf_exempt
from .models import User, Token, Income, Expense, UserRegister, Slider, News
from datetime import datetime
from django.views import generic


from django.core import serializers
from django.contrib.auth.hashers import make_password
from django.db.models import Sum
from django.utils.crypto import get_random_string
import random
from django.contrib.auth.decorators import login_required
from .utils import grecaptcha_verify
import string
# from postmark import PMMail

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login

import requests
from bs4 import BeautifulSoup as soup
import time


def index(request):
    context = {}
    
    count_of_users = User.objects.all().count()
    context["count_of_users"] = count_of_users
    
    
    def getPrices():
        
        response = requests.get("https://arzdigital.com/coins/bitcoin/")
        HTML = soup(response.text, "html.parser")

        response2 = requests.get("https://arzdigital.com/coins/ethereum/")
        HTML2 = soup(response2.text, "html.parser")
        
        toman = HTML.find("span", attrs = {"class" : "arz-sana-price"})
        btc = HTML.find("div", attrs = {"class" : "arz-coin-page-data-coin-price coinPrice btcprice pulser"})
        eth = HTML2.find("div", attrs = {"class" : "arz-coin-page-data-coin-price coinPrice pulser"})

        context["toman"] = toman.text
        context["btc"] = btc.text
        context["eth"] = eth.text     
        
    
    def setSlider():
        slider = get_list_or_404(Slider)
        
        context["slider"] = slider
        return context
    
    
    def setNews():
        news = get_list_or_404(News)
        context["news"] = news
            
        return context

    
        
    # get toman and btc and eth prices 
    # getPrices()
    
    # send image and caption to template
    setSlider()
    
    # send news to template
    setNews()
    
    
    return render(request, "web/index.html", context)

# create random string for Token
random_str = lambda N: ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(N))

from django.conf import settings

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
            first_name = request.POST["first_name"]
            email = request.POST['email']
            
            # hash passwords
            password = make_password(request.POST['password'])
            passwordConfirm = make_password(request.POST['passwordConfirm'])
            username = request.POST['username']
            
            ps1 = request.POST['password']
            ps2 = request.POST['passwordConfirm']
            # check passwords
            if not ps1 == ps2:
                context = {
                    "message" : "عدم تطابق رمز عبور مجددا تلاش کنید"
                }
                return render(request, 'registration/register.html', context)
            
            else:                
                
                temporarycode = UserRegister(
                    email=email, time=now, code=code, username=username, password=password,
                    firstName = first_name, passwordConfirm = passwordConfirm)
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
                message = "برای فعال کردن اکانت بستون خود <a href=\"{0}?code={1}\">اینجا</a> کلیک کنید".format(request.build_absolute_uri('/register/'), code)
                context = {
                    'message': message 
                    }
                return render(request, 'registration/register.html', context)
        
        else:
            context = {
                'message': 'متاسفانه این نام کاربری قبلا استفاده شده است. از نام کاربری دیگری استفاده کنید.'}  # TODO: forgot password
            # TODO: keep the form data
            return render(request, 'registration/register.html', context)
        
    elif "code" in request.GET:  # user clicked on code
        code = request.GET['code']
        if UserRegister.objects.filter(code=code).exists():  # if code is in temporary db, read the data and create the user
            new_temp_user = UserRegister.objects.get(code=code)
            newuser = User.objects.create(username=new_temp_user.username, password=new_temp_user.password,
                                          email=new_temp_user.email, first_name = new_temp_user.firstName)
            this_token = get_random_string(length=48)
            token = Token.objects.create(user=newuser, token=this_token)
            # delete the temporary activation code from db
            UserRegister.objects.filter(code=code).delete()
            
            message = "اکانت شما ساخته شد برای ورود <a href=/{}>اینجا</a> کلیک کنید".format("login")
            context = {
                "message" : message    
            }
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

    
    
    return JsonResponse({
       "status" : "ok",
       "M" : request.POST
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
    
    
    def deleteField():        
        if request.POST:
            this_user = request.user
            this_id = int(request.POST["this_id"])
            
            if request.POST["kind_of_field"] == "exD":           
                Expense.objects.filter(user = this_user).filter(id = this_id).delete()
            elif request.POST["kind_of_field"] == "enD":
                Income.objects.filter(user = this_user).filter(id = this_id).delete()
    
    
    def updateField():        
        if request.POST:
            this_user = request.user
            this_id = int(request.POST["this_id"])
            
            if request.POST["kind_of_field"] == "exU": 
                this_toman = request.POST["this_toman"]
                this_titr = request.POST["this_titr"]          
                Expense.objects.filter(user = this_user).filter(id = this_id).update(amount = this_toman, 
                           text = this_titr)
                
            elif request.POST["kind_of_field"] == "enU":
                this_toman = request.POST["this_toman"]
                this_titr = request.POST["this_titr"]
                Income.objects.filter(user = this_user).filter(id = this_id).update(amount = this_toman, 
                           text = this_titr)
           
            
    
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
    
    # for delete fields
    deleteField()
    
    # for update fields
    updateField()
    
    return render(request, "web/dashboard_status.html", context)
    
    
 
@login_required
def dashboard(request):
    
    this_user = request.user
    now = datetime.now()
    context  = {}
    
    def setExpese():
        if "text" in request.POST and "amount" in request.POST :
            
            this_text = request.POST["text"]
            this_amount = request.POST["amount"]
                
            if not "this_date" in request.POST:
                this_date = datetime.now()
            else:
                this_date = request.POST["this_date"]
            
            post_content = Expense(user = this_user, text = this_text, amount = this_amount,
                                    date=this_date)
            post_content.save()
    
    
    def setIncome():
        if "text" in request.POST and "amount" in request.POST :
            
            this_text = request.POST["text"]
            this_amount = request.POST["amount"]
                
            if not "this_date" in request.POST:
                this_date = datetime.now()
            else:
                this_date = request.POST["this_date"]
            
            post_content = Income(user = this_user, text = this_text, amount = this_amount,
                                    date=this_date)
            post_content.save()
            
        
    if "expense" in request.POST:
        setExpese()
        
    elif "income" in request.POST:
        setIncome()
    
    
    context["now"] = now
    
    return render(request, "web/dashboard.html", context)


