import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from program.model.write_db import Write_db
from program.model.read_db import Read_db


class Controller:
    def __init__(self) -> None:
        self.write_db = Write_db()
        self.read_db = Read_db()

    #Reade_db methods
    def authenticate_user(self, user_id, password):
        return self.read_db.authenticate_user(user_id, password)
    def get_user_id(self, user_id):
        return self.read_db.get_user_id(user_id)
    def get_password(self, user_id):
        return self.read_db.get_password(user_id)
    def get_events(self):
        return self.read_db.get_events()
    def get_enrolled_events(self, user_id):
        return self.read_db.get_enrolled_events(user_id)
    def get_company_name(self, event_id):
        return self.read_db.get_company_name(event_id)
    def get_event_data(self, event_id):
        return self.read_db.get_event_data(event_id)
    
    # Write_db methods
    def insert_new_user(self, user_id, password, admin=False):
        self.write_db.insert_new_user(user_id, password, admin)
    def change_user_id(self, user_id, user_id_new):
        self.write_db.change_user_id(user_id, user_id_new)
    def change_password(self, user_id, password):
        self.write_db.change_password(user_id, password)
    def remove_account(self, user_id):
        self.write_db.remove_account(user_id)
    def register_enrollment(self, event_id, user_id):
        return self.write_db.register_enrollment(event_id, user_id)
    def unenroll(self, event_id, user_id):
        return self.write_db.unenroll(event_id, user_id)
