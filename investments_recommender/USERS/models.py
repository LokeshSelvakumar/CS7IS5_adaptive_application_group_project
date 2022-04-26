from django.db import models
import numpy as np
import string
import random
# # Create your models here.
# class Users(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=20)
#     age = models.IntegerField()
#     gender = models.CharField(choices=(('MALE','Male'), ('FEMALE','Female')))
#     email = models.EmailField()
#     occupation = models.CharField(choices= (('ENGINEER', 'engineer'),
#                                             ('DOCTOR', 'doctor'),
#                                             ))
#     salary = models.CharField(choices= (('Poor','5000-25000(Before EMIs)'),
#                                         ('Middle class','20000-80000(Before EMIs)'),
#                                         ('homeless','No steady income'),
#                                         ('Rich','I am rich'),
#                                         ))

# # class to maintain all the preferences
# class Preferences(Users):
#     stocks_invested = [Stocks]
#     watchlist_stocks = [Stocks]
#     news_interested = [News]
#     preferred_source = models.CharField(choices=(('YAHOO', 'yahoo'),
#                                                 ('GOOGLE', 'google'),
#        
#                                          ))

class User:

    def __init__(self,user_data):
        self.user_id = user_data['user_id']
        self.name = user_data['name']
        self.age = user_data['age']
        self.gender = user_data['sex']
        self.email = user_data['email']
        self.salary = user_data['salary']

        self.stockslist = user_data['stocksList']
        self.watchlist = user_data['watchList']
        self.risk_score = user_data['score_risk']
        self.available_capital = user_data['avail_capital']
        self.sector_preference = {
            0:"Technology",
            1:"Industrials",
            2:"Financial Services",
            4:"Healthcare",
            3:"Consumer Cyclical",
            5:"Consumer Defensive ",
            6:"Real Estate ",
            7:"Utilities",
            8:"Communication Services",
            9:"Basic Materials ",
            10:"Energy",
        }
        self.risk_preference = self.calculate_risk_preference()
        self.password = self.generate_random_password()

    def update_sector_preference(self):
        return "Success"
        
    def update_risk_preference(self):
        return "Success"

    def calculate_risk_preference(self):
        if self.risk_score < 12:
            return "low_risk"
        elif self.risk_score >18:
            return "high_risk"
        else:
            return "moderate_risk"

    def generate_random_password(self):
        ## characters to generate password from
        characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
        ## length of password from the user
        length = 5

        ## shuffling the characters
        random.shuffle(characters)
        
        ## picking random characters from the list
        password = []
        for i in range(length):
            password.append(random.choice(characters))

        ## shuffling the resultant password
        random.shuffle(password)

        ## converting the list to string
        ## printing the list
        return "".join(password)

    def toJSON(self):
        result = {}
        result['user_id'] = self.user_id
        result['name'] = self.name
        result['age'] = self.age
        result['gender'] = self.gender
        result['email'] = self.email
        result['salary'] = self.salary
        result['sector_preference'] = self.sector_preference
        result['available_capital'] = self.available_capital
        result['risk_preference'] = self.risk_preference
        result['password'] = self.password
        return result
        
        
        
        
        
        
        
        
        
