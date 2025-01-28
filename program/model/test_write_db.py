import unittest
from unittest.mock import patch, MagicMock
from write_db import Write_db

class TestWriteDb(unittest.TestCase):

    def setUp(self):
        self.mock_database = MagicMock()
        self.write_db = Write_db()
        self.write_db.database = self.mock_database

    def test_insert_new_user(self):
        mock_user_data = {"Password" : "test_password", "Admin": "false"}
        self.write_db.insert_new_user("test_user", "test_password", "false")
        self.mock_database.child("Users").child("test_user").set.assert_called_once_with(mock_user_data)

    def test_change_user_id(self):
        test_old_user = "old_username"
        test_new_user = "new_username"
        mock_user_data = {"Password" : "test_password", "Admin": "false"}
        self.mock_database.child("Users").child(test_old_user).get.return_value.val.return_value = mock_user_data

        self.write_db.change_user_id(test_old_user, test_new_user)

        self.mock_database.child("Users").child(test_new_user).set.assert_called_once_with(mock_user_data)
        self.mock_database.child("Users").child(test_old_user).remove.assert_called_once()


    def test_change_password(self):
        test_user_id = "test_user"
        new_password = "new_secure_password"

        self.write_db.change_password(test_user_id, new_password)

        self.mock_database.child("Users").child(test_user_id).update.assert_called_once_with({"Password": new_password})

    def test_remove_account(self):
        test_user_id = "test_user"
        self.write_db.remove_account(test_user_id)

        self.mock_database.child("Users").child(test_user_id).remove.assert_called_once()

    

    def test_register_enrollment(self):
        test_user_id = "test_user"
        test_event_id = 300

        mock_user_data = {"Admin": "false", "Password": "test_password", "enrolled_events": [5, 1, 3]}
        mock_event_data = {"date": "2024-01-01", "name": "Event A", "company_name": "Test Charity Name", "enrolled_users": ["user1", "user2"]}

        self.mock_database.child("Users").child(test_user_id).get.return_value.val.return_value = mock_user_data
        self.mock_database.child("Users").child(test_event_id).get.return_value.val.return_value = mock_event_data

        successful_registration = self.write_db.register_enrollment(test_event_id, test_user_id)

        self.assertTrue(successful_registration)

    def test_unenroll_success(self):
        test_user_id = "test_user"
        test_event_id = 300
        mock_user_data = {"Admin": "false", "Password": "test_password", "enrolled_events": [5, 1, 3]}
        mock_event_data = {"date": "2024-01-01", "name": "Event A", "company_name": "Test Charity Name", "enrolled_users": ["user1", "user2"]}

        result = self.write_db.unenroll(test_event_id, test_user_id)

        self.assertTrue(result)

    def test_unenroll_data_not_found(self):
        test_user_id = "test_user"
        test_event_id = 300
        mock_user_data = None
        mock_event_data = None

        self.mock_database.child("Users").child(test_user_id).get.return_value.val.return_value = mock_user_data
        self.mock_database.child("Users").child(test_event_id).get.return_value.val.return_value = mock_event_data

        result = self.write_db.unenroll(test_event_id, test_user_id) 

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()