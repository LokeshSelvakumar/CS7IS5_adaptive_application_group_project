from django.shortcuts import render
from .models import User
from ..investments_recommender.static import firebaseInitialization


# Create your views here.
def create_user(request):
    user_id = request.body['id']
    name = request.body['name']
    age = request.body['age']
    gender = request.body['gender']
    email = request.body['email']
    occupation = request.body['occupation']
    salary = request.body['salary']
    firebaseInitialization.save_user(user_id, name, age, gender, email, occupation, salary)
