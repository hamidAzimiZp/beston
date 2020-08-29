from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from json.encoder import JSONEncoder
from django.views.decorators.csrf import csrf_exempt
from .models import User, Token, Income, Expense
from datetime import datetime


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