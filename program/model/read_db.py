import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import pyrebase
import json

class Read_db:
    def __init__(self):
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json'))

        with open(config_path ,'r') as config_file:
            config = json.load(config_file)

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
    
    def get_events(self):
        events = self.database.child("Events").get()
        if events.val() is not None:
            
            events_list = [event for event in events.val() if event is not None]
            sorted_events = sorted(events_list, key=lambda x: x["date"])

            return sorted_events
        return None

    def get_enrolled_events(self, user_id):
        user_data = self.database.child("Users").child(user_id).get()
        if user_data.val() is not None:
            data = user_data.val()
            return data.get('enrolled_events', [])
        else:
            return []


    def get_company_name(self, event_id):
        company_data = self.database.child("Events").child(event_id).get()
        if company_data.val() is not None:
            data = company_data.val()
            return data.get('company_name', "")
        return ""


    def get_event_data(self, event_id):
        event_data = self.database.child("Events").child(event_id).get()
        if event_data.val() is not None:
            return event_data.val()
        return []
