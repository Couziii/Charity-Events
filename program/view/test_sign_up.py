import unittest
from unittest.mock import MagicMock
from PyQt5.QtWidgets import QApplication
from sign_up import UI_signup_window

class TestUISignupWindow(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])


    def setUp(self):
        self.window = UI_signup_window()

        self.window.controller = MagicMock()

        self.signal_mock = MagicMock()
        self.window.signal_object.connect(self.signal_mock)
    

    ### UNIT TESTS ###


    def test_btn_cancel_clicked(self):
        
        self.window.txt_user_id.setText("testuser")
        self.window.txt_password.setText("password123")
        self.window.txt_admin_code.setText("admincode")

        self.window.btn_cancel_clicked()

        self.assertEqual(self.window.txt_user_id.text(), "")
        self.assertEqual(self.window.txt_password.text(), "")
        self.assertEqual(self.window.txt_admin_code.text(), "")

        self.signal_mock.assert_called_once()

        self.assertFalse(self.window.isVisible())


    def test_btn_signup_clicked(self):

        self.window.txt_user_id.setText("validuser")
        self.window.txt_password.setText("validpassword")
        self.window.txt_admin_code.setText("")

        self.window.controller.get_user_id.return_value = None

        self.window.btn_signup_clicked()

        self.window.controller.insert_new_user.assert_called_once_with("validuser", "validpassword")

        self.signal_mock.assert_called_once()

        self.assertFalse(self.window.isVisible())


    def test_btn_signup_clicked_invalid_input(self):

        self.window.txt_user_id.setText("invalid'user")
        self.window.txt_password.setText("")
        self.window.txt_admin_code.setText("wrongcode")

        self.window.controller.get_user_id.return_value = None

        self.window.btn_signup_clicked()

        self.assertEqual(self.window.lbl_unavailable_user_id.text(), "No injection symbols allowed")
        self.assertEqual(self.window.lbl_unauthorized_password.text(), "Password must not be empty!")

        self.assertTrue(self.window.wrong_inputs)

        self.window.controller.insert_new_user.assert_not_called()

        self.signal_mock.assert_not_called()


    def test_check_input_valid(self):

        self.window.txt_user_id.setText("validuser")
        self.window.txt_password.setText("validpassword")
        self.window.txt_admin_code.setText("")

        self.window.controller.get_user_id.return_value = None

        self.window.check_input()

        self.assertFalse(self.window.wrong_inputs)

        self.assertEqual(self.window.lbl_unavailable_user_id.text(), "")
        self.assertEqual(self.window.lbl_unauthorized_password.text(), "")
        self.assertEqual(self.window.lbl_wrong_admin_code.text(), "")
    

    def test_check_input_invalid(self):

        self.window.txt_user_id.setText("invalid'user")
        self.window.txt_password.setText("")
        self.window.txt_admin_code.setText("wrongcode")

        self.window.controller.get_user_id.return_value = "exists"

        self.window.check_input()

        self.assertTrue(self.window.wrong_inputs)

        self.assertEqual(self.window.lbl_unavailable_user_id.text(), "User ID already exists")
        self.assertEqual(self.window.lbl_unauthorized_password.text(), "Password must not be empty!")
        

    def test_clear_window(self):

        self.window.txt_user_id.setText("user")
        self.window.txt_password.setText("pass")
        self.window.txt_admin_code.setText("code")

        self.window.lbl_unavailable_user_id.setText("Error")
        self.window.lbl_unauthorized_password.setText("Hello")
        self.window.lbl_wrong_admin_code.setText("No")

        self.window.clear_window()

        self.assertEqual(self.window.txt_user_id.text(), "")
        self.assertEqual(self.window.txt_password.text(), "")
        self.assertEqual(self.window.txt_admin_code.text(), "")
        self.assertEqual(self.window.lbl_unavailable_user_id.text(), "")
        self.assertEqual(self.window.lbl_unauthorized_password.text(), "")
        self.assertEqual(self.window.lbl_wrong_admin_code.text(), "")


    @classmethod
    def tearDownClass(cls):
        cls.app.quit()


if __name__ == "__main__":
    unittest.main()
    