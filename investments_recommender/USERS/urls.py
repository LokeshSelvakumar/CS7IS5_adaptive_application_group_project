from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path("createUser/",views.create_user),
    path("verify/",views.verify_user),
]