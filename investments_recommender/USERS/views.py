from django.http import JsonResponse
from django.shortcuts import render
from investments_recommender.static import firebaseInitialization
from .models import User
from firebase_admin import db
import json

# Create your views here.
#Sample User Data:
# user_data = {
#     'user_id' : 111,
#     'sector_preference' : [
#         'Technology'
#     ],
#     'available_captial': 2000,
#     'age' : 20,
#     'risk_preference': 'low_risk'
# }
def save_user_to_fb(user):
    try:
        ref = db.reference("/Users")
        ref.update({
            user['user_id']: {
                "Name": user['name'],
                "Age":  user['age'],
                "Gender": user['gender'],
                "Email": user['email'],
                "Salary Range": user['salary'],
                "sector_preference": user['sector_preference'],
                "available_capital": user['available_capital'],
                "risk_preference": user['risk_preference'],
                "password": user['password'],
            }
        })
        return True
    except:
        return False

def create_user(request):
    user_data = json.loads(request.body)
    new_user = User(user_data=user_data)
    print(new_user.toJSON())
    # user_data = request.body.text
    # new_user = User(user_data=user_data)
    status = save_user_to_fb(new_user.toJSON())
    if status:
        return JsonResponse({"status":"New User Added successfully","password":new_user.password})
    else:
        return JsonResponse({"status":"Failed."})

def verify_user(request):
    user_data = json.loads(request.body)
    user_id = str(user_data['user_id'])
    password = user_data['password']
    ref = db.reference("/Users")
    users = ref.get()
    isVerifiedUser = False
    print(users[user_id]['password'])
    if user_id in users.keys():
        isVerifiedUser = (users[user_id]['password'] == password)
    return JsonResponse({"status":isVerifiedUser})

