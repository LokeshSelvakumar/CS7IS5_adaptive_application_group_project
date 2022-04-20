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
ref = db.reference("/")
ref.set({"Users": {
    "user_id1": {
        "Name": "Jack",
        "Username": "jack"
    }
}})
ref.update({"Users": {
    "user_id2": {
        "Name": "Lucy",
        "Username": "lucy"
    }
}})