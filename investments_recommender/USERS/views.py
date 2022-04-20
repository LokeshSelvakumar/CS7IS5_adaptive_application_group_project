from django.shortcuts import render
from .models import User

# Create your views here.
def create_user(request):
    new_user = request.body
    User.save(new_user)
