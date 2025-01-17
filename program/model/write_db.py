import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import pyrebase


class Write_db:
    def __init__(self):
        config = {"apiKey": "AIzaSyBYJZmYSMs_KGrTFDjFRvb3n3rKXqnCoyM",
                  "authDomain": "charityapp-998a9.firebaseapp.com",
                  "databaseURL": "https://charityapp-998a9-default-rtdb.europe-west1.firebasedatabase.app",
                  "projectId": "charityapp-998a9",
                  "storageBucket": "charityapp-998a9.firebasestorage.app",
                  "messagingSenderId": "386609417916",
                  "appId": "1:386609417916:web:46df689fe99b051f2c0ab9",
                  "measurementId": "G-HT63HBBW90"}
        firebase = pyrebase.initialize_app(config)
        self.database = firebase.database()

    def insert_new_user(self, user_id, password, admin):
        user_info = {"Password" : password, "Admin" : admin}
        self.database.child("Users").child(user_id).set(user_info)

    def change_user_id(self, old_user_id, new_user_id):
        user_data = self.database.child("Users").child(old_user_id).get()
        if user_data.val() is not None:
            self.database.child("Users").child(new_user_id).set(user_data.val())
            self.database.child("Users").child(old_user_id).remove()

    def change_password(self, user_id, password):
        self.database.child("Users").child(user_id).update({"Password":password})
    
    def remove_account(self, user_id):
        self.database.child("Users").child(user_id).remove()