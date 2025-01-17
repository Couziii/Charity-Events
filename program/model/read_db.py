import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import pyrebase


class Read_db:
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

    def authenticate_user(self, user_id, password):
        users = self.database.child("Users").get()
        if users.val() is not None:  # Check if there are any users in the database
            for uid, user_info in users.val().items():
                if uid == user_id:  # Check if the user_id matches
                    if user_info["Password"] == password:  # Check if the password matches
                        return True
        return False  # Return False if user_id is not found or password doesn't match
    
    def get_user_id(self, user_id):
        users = self.database.child("Users").get()
        if users.val() is not None:  # Check if there are any users in the database
            for uid, user_info in users.val().items():
                if uid == user_id:  # Compare with the correct variable
                    return uid, user_info
        return None  # Return None if user_id is not found
    
    def get_password(self, user_id):
        user_data = self.database.child("Users").child(user_id).get()
        if user_data.val() is not None:  # Check if user data exists
            return user_data.val().get("Password")  # Retrieve and return the password
        return None  # Return None if user does not exist