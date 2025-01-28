import unittest
from unittest.mock import patch, MagicMock
from read_db import Read_db

class TestReadDb(unittest.TestCase):

    def setUp(self):
        self.mock_database = MagicMock()
        self.read_db = Read_db()
        self.read_db.database = self.mock_database

    def test_authenticate_user(self):
        mock_user_data = {
            "test_user": {"Admin": "false", "Password": "test_password"},
            "test_user_2": {"Admin": "false", "Password": "test_password_2"}
        }

        self.mock_database.child("Users").get.return_value.val.return_value = mock_user_data

        result = self.read_db.authenticate_user("test_user_2", "test_password_2")

        self.assertTrue(result)

    def test_authenticate_user_invalid_password(self):
        mock_user_data = {
            "test_user": {"Admin": "false", "Password": "test_password"},
            "test_user_2": {"Admin": "false", "Password": "test_password_2"}
        }

        self.mock_database.child("Users").get.return_value.val.return_value = mock_user_data

        result = self.read_db.authenticate_user("test_user_2", "invalid_password")
        self.assertFalse(result)

    def test_authenticate_user_empty_database(self):

        self.mock_database.child("Users").get.return_value.val.return_value = None

        result = self.read_db.authenticate_user("test_user", "test_password")

        self.assertFalse(result)

    def test_get_user_id_valid_user(self):
        mock_user_data = {
        "test_user": {"Admin": "false", "Password": "test_password"},
        "test_user_2": {"Admin": "false", "Password": "test_password_2"}
    }

        self.mock_database.child("Users").get.return_value.val.return_value = mock_user_data

        result = self.read_db.get_user_id("test_user")

        expected = ("test_user", {"Admin": "false", "Password": "test_password"})

        self.assertEqual(result, expected)

    def test_get_user_id_invalid_user(self):
        mock_user_data = {
        "test_user": {"Admin": "false", "Password": "test_password"},
        "test_user_2": {"Admin": "false", "Password": "test_password_2"}
    }

        self.mock_database.child("Users").get.return_value.val.return_value = mock_user_data

        result = self.read_db.get_user_id("invalid_username")

        self.assertIsNone(result)

    def test_get_password(self):
        mock_user_data = {"Admin": "false", "Password": "test_password", "enrolled_events": [5, 1, 3]}

        self.mock_database.child("Users").child("test_user").get.return_value.val.return_value = mock_user_data

        result = self.read_db.get_password("test_user")
        expected = "test_password"

        self.assertEqual(result, expected)
        self.mock_database.child("Users").child("test_user").get.assert_called_once()

    def test_get_events(self):
        mock_events = [
            None,
            {"date": "2024-01-01", "name": "Event A"},
            {"date": "2024-01-03", "name": "Event C"},
            {"date": "2024-01-02", "name": "Event B"},
        ]

        self.mock_database.child("Events").get.return_value.val.return_value = mock_events

        result = self.read_db.get_events()

        expected = [
            {"date": "2024-01-01", "name": "Event A"},
            {"date": "2024-01-02", "name": "Event B"},
            {"date": "2024-01-03", "name": "Event C"},
        ]

        self.assertEqual(result, expected)
        self.mock_database.child("Events").get.assert_called_once()
    
    def test_get_enrolled_events(self):
        mock_user_data = {"Admin": "false", "Password": "test", "enrolled_events": [5, 1, 3]}
        self.mock_database.child("Users").child("test_user").get.return_value.val.return_value = mock_user_data

        result = self.read_db.get_enrolled_events("test_user")
        expected = [5, 1, 3]

        self.assertEqual(result, expected)
        self.mock_database.child("Users").child("test_user").get.assert_called_once()

    def test_get_company_name(self):
        mock_event_data = {"date": "2024-01-01", "name": "Event A", "company_name": "Test Charity Name"}
        self.mock_database.child("Events").child("test_event").get.return_value.val.return_value = mock_event_data

        result = self.read_db.get_company_name("test_event")

        expected = "Test Charity Name"
        self.assertEqual(result, expected)
        self.mock_database.child("Events").child("test_event").get.assert_called_once()


    def test_get_event_data(self):
        mock_event_data = {"date": "2024-01-01", "name": "Event A", "company_name": "Test Charity Name"}
        self.mock_database.child("Events").child("test_event").get.return_value.val.return_value = mock_event_data 

        result = self.read_db.get_event_data("test_event")

        self.assertEqual(result, mock_event_data)
        self.mock_database.child("Events").child("test_event").get.assert_called_once()

    
if __name__ == "__main__":
    unittest.main()