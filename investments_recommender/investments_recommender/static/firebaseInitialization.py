import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
import os

privatekeypath = os.path.join(os.getcwd(),'')
privPath = os.path.join(privatekeypath,'privateKey.json')
cred_obj = credentials.Certificate(privPath)

default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': 'https://investment-recommender-default-rtdb.europe-west1.firebasedatabase.app/'
})
# ref = db.reference("/Users")
# ref = db.reference("/Reference")


def save_user(user_id, name, age, gender, email, occupation="", salary=""):
    ref = db.reference("/Users")
    ref.update({
        user_id: {
            "Name": name,
            "Age":  age,
            "Gender": gender,
            "Email": email,
            "Occupation": occupation,
            "Salary Range": salary
        }
    })


def save_reference(user_id, reference="", knowledge="", news="", stock=""):
    ref = db.reference("/Reference")
    ref.update({
        user_id:{
            "reference field": reference,
            "knowledge": knowledge,
            "news": news,
            "stock": stock
        }
    })


def query_user(user_id):
    ref = db.reference("/user").child(user_id)
    name = ref.child("Name").get()
    age = ref.child("Age").get()
    gender = ref.child("Gender").get()
    email = ref.child("Name").get()
    occupation = ref.child("Occupation").get()
    salary = ref.child("Salary").get()


def query_reference(user_id):
    ref = db.reference("/Reference").child(user_id)
    reference = ref.child("reference field").get()
    knowledge = ref.child("knowledge").get()
    news = ref.child("news").get()
    stock = ref.child("stock").get()

# save_user("12345", "KiKi", 24, "Female", "123@tcd.ie", "doctor", "")
# save_reference("12345","energy", "medical", "Energy", "Meta")

