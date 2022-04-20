from django.db import models

from ..STOCKS_HANDLER.models import Stocks
from ..NEWS_HANDLER.models import News

# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    gender = models.CharField(choices=(('MALE','Male'), ('FEMALE','Female')))
    email = models.EmailField()
    occupation = models.CharField(choices= (('ENGINEER', 'engineer'),
                                            ('DOCTOR', 'doctor'),
                                            ))
    salary = models.CharField(choices= (('Poor','5000-25000(Before EMIs)'),
                                        ('Middle class','20000-80000(Before EMIs)'),
                                        ('homeless','No steady income'),
                                        ('Rich','I am rich'),
                                        ))

# class to maintain all the preferences
class Preferences(Users):
    stocks_invested = [Stocks]
    watchlist_stocks = [Stocks]
    news_interested = [News]
    preferred_source = models.CharField(choices=(('YAHOO', 'yahoo'),
                                                ('GOOGLE', 'google'),
                                                ))
