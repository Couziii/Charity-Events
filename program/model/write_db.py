import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import pyrebase
import json

class Write_db:
    def __init__(self):
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json'))

        with open(config_path ,'r') as config_file:
            config = json.load(config_file)

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
    
    def register_enrollment(self, event_id, user_id):
        ''' Updates the users and events collections to show an enrollment. '''
        try:
            user_data = self.database.child("Users").child(user_id).get()
            event_data = self.database.child("Events").child(event_id).get()

            if user_data.val() is not None and event_data.val() is not None:
                enrolled_events = user_data.val().get("enrolled_events", [])
                enrolled_users = event_data.val().get("enrolled_users", [])

                if event_id not in enrolled_events:
                    enrolled_events.append(event_id)
                    self.database.child("Users").child(user_id).update({"enrolled_events": enrolled_events})
                
                if user_id not in enrolled_users:
                    enrolled_users.append(user_id)
                    self.database.child("Events").child(event_id).update({"enrolled_users": enrolled_users})
                
                return True

            else:
                return False

        except Exception as e:
            print("Error during registering enrollment", e)
            return False

    def unenroll(self, event_id, user_id):
        ''' Updates the users and events collections to no longer show the enrollment. '''
        try:
            user_data = self.database.child("Users").child(user_id).get()
            event_data = self.database.child("Events").child(event_id).get()

            if user_data.val() is not None and event_data.val() is not None:
                enrolled_events = user_data.val().get("enrolled_events", [])
                enrolled_users = event_data.val().get("enrolled_users", [])

                if event_id in enrolled_events:
                    enrolled_events.remove(event_id)
                    self.database.child("Users").child(user_id).update({"enrolled_events": enrolled_events})
                
                if user_id in enrolled_users:
                    enrolled_users.remove(user_id)
                    self.database.child("Events").child(event_id).update({"enrolled_users": enrolled_users})
                
                return True
            
            else:
                return False
        
        except Exception as e:
            print("Error during unenrollment", e)
            return False
                