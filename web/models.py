from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Expense(models.Model):
    text = models.CharField(max_length = 300)
    date = models.DateTimeField()
    amount = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True, blank = True)
    
    
    class Meta:
        ordering = ["date", "amount"]
        
    
    def __str__(self):
        return "{0}  <{1} T>".format(self.text, self.amount)
    
    
class Income(models.Model):
    text = models.CharField(max_length = 300)
    date = models.DateTimeField()
    amount = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True, blank = True)
    
    
    class Meta:
        ordering = ["date", "amount"]
        
    
    def __str__(self):
        return "{0}  <{1} T>".format(self.text, self.amount)