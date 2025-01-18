import unittest
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton
from login import UI_login_window

class TestUILoginWindow(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):

        self.window = UI_login_window()

        self.window.btn_login = MagicMock(spec=QPushButton)
        self.window.txt_user_id = MagicMock(spec=QLineEdit)
        self.window.txt_password = MagicMock(spec=QLineEdit)
        self.window.lbl_wrong_input = MagicMock(spec=QLabel)
        self.window.lbl_signup = MagicMock(spec=QLabel)

        self.window.controller = MagicMock()

        self.window.user_id = "test_user"
    
    ### UNIT TESTS ###


    def test_widgets_loaded_correctly(self):
        self.assertIsNotNone(self.window.btn_login, "btn_login not loaded")
        self.assertIsNotNone(self.window.txt_user_id, "txt_user_id not loaded")
        self.assertIsNotNone(self.window.txt_password, "txt_password not loaded")
        self.assertIsNotNone(self.window.lbl_wrong_input, "lbl_wrong_input not loaded")
        self.assertIsNotNone(self.window.lbl_signup, "lbl_signup not loaded")


    def test_widget_connections(self):
        with patch.object(self.window.btn_login, "clicked") as mock_signal:

            self.window.btn_login.clicked.connect(self.window.btn_login_clicked)

            mock_signal.connect.assert_called_once_with(self.window.btn_login_clicked)
    

    def test_btn_login_clicked_success(self):
        self.window.wrong_inputs = False

        self.window.check_input = MagicMock()
        self.window.clear_window = MagicMock()
        self.window.close = MagicMock()

        with patch("login.UI_main_window") as MockMainWindow:
            mock_instance = MockMainWindow.return_value
            mock_instance.signal_object.connect = MagicMock()

            self.window.btn_login_clicked()

            self.window.check_input.assert_called_once()

            MockMainWindow.assert_called_once_with(self.window, self.window.user_id)

            mock_instance.signal_object.connect.assert_called_once_with(self.window.show)

            self.window.clear_window.assert_called_once()
            self.window.close.assert_called_once()
            mock_instance.show.assert_called_once()
    

    def test_check_input_valid(self):
    
        self.window.get_window_values = MagicMock()

        self.window.user_id = "valid_user"
        self.window.password = "valid_password"

        self.window.controller.authenticate_user.return_value = True

        self.window.check_input()

        self.assertFalse(self.window.wrong_inputs)
    

    def test_check_input_invalid(self):
        
        self.window.get_window_values = MagicMock()

        self.window.user_id = "invalid'"
        self.window.password = "still_valid_password"

        self.window.check_input()

        self.window.lbl_wrong_input.setText.assert_called_once_with("No injection symbols allowed")

        self.assertTrue(self.window.wrong_inputs)


    def test_get_window_values(self):

        self.window.txt_user_id.text.return_value = "test_user"
        self.window.txt_password.text.return_value = "test_password"

        self.window.get_window_values()

        self.assertEqual(self.window.user_id, "test_user")
        self.assertEqual(self.window.password, "test_password")

    
    def test_clear_window(self):

        self.window.clear_window()

        self.window.txt_user_id.clear.assert_called_once()
        self.window.txt_password.clear.assert_called_once()

        self.window.lbl_wrong_input.setText.assert_called_once_with("")
    

    def test_lbl_signup_clicked(self):
        
        self.window.clear_window = MagicMock()
        self.window.close = MagicMock()

        with patch("login.UI_signup_window") as MockSignupWindow:
            mock_instance = MockSignupWindow.return_value
            mock_instance.signal_object.connect = MagicMock()

            self.window.lbl_signup_clicked()

            MockSignupWindow.assert_called_once_with(self.window)

            mock_instance.signal_object.connect.assert_called_once_with(self.window.show)

            self.window.clear_window.assert_called_once()
            self.window.close.assert_called_once()
            mock_instance.show.assert_called_once()


    @classmethod
    def tearDownClass(cls):
        cls.app.quit()
    
    
if __name__ == "__main__":
    unittest.main()
