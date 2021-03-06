from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models import OneToOneField
import datetime
from django.conf import settings

class UserRegister(models.Model):
    code = models.CharField(max_length=32)
    firstName = models.CharField(max_length = 32, blank = True)
    email = models.CharField(max_length=120)
    time = models.DateTimeField(default=datetime.date.today)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)  # TODO: do not save password
    passwordConfirm = models.CharField(max_length=50, blank = True)
    
    def __str__(self):
        return self.username


class Member(models.Model):
    code = models.CharField(max_length=32)
    email = models.CharField(max_length=120)
    time = models.DateTimeField(default=datetime.date.today)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)  # TODO: do not save password
    
    
    def __str__(self):
        return self.username
    
    
class Token(models.Model):
    user = OneToOneField(User, on_delete = models.CASCADE)
    token = models.CharField(max_length = 36)
    
    
    def __str__(self):
        return "{}_token".format(self.user)
    

class Expense(models.Model):
    text = models.CharField(max_length = 300)
    date = models.DateTimeField()
    amount = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank = True)
    
    
    class Meta:
        ordering = ["id", "date", "amount"]
        
    
    def __str__(self):
        return "<{0}> {1}  <{2} T>".format(self.user, self.text, self.amount)
    
    
class Income(models.Model):
    text = models.CharField(max_length = 300)
    date = models.DateTimeField()
    amount = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True, blank = True)
    
    
    class Meta:
        ordering = ["id", "date", "amount"]
        
    
    def __str__(self):
        return "<{0}>-({1})-<{2} T>".format(self.user, self.text, self.amount)
    

class Slider(models.Model):
    caption = models.CharField(max_length = 100, help_text = "optional", null = True, blank = True)
    image = models.ImageField(upload_to = "static/_images/slider/")
    date = models.DateTimeField()
    
    
    class Meta:
        ordering = ["id", "date"]
        
    
    def __str__(self):
        return "{}".format(self.image)
    
    
class News(models.Model):
    
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length =250, blank = True)
    description = models.CharField(max_length=450, blank = True)
    text = models.TextField()
    image = models.ImageField(upload_to = "static/_images/news/", blank = True)
    date = models.DateTimeField()
    
    
    class Meta:
        ordering = ["date"]
        
        
    def __str__(self):
        return "{}  <{}>".format(self.title, self.date)