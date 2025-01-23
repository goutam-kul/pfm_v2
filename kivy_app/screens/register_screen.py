from kivymd.uix.screen import MDScreen
from kivy_app.utils import DialogMixin
import requests

class RegisterScreen(MDScreen, DialogMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dialog = None

    def register_user(self, username, email, password, confirm_password):
        if password != confirm_password:
            self.show_message("Error", "Passwords do not match.")
            return

        url = "http://127.0.0.1:6000/users/register"
        payload = {
            "username": username.strip(),
            "email": email.strip(),
            "password": password.strip()
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                self.show_message("Success", "Registration successful! Please log in.")
            else:
                error_detail = response.json().get("detail", "Unknown error")
                self.show_message("Error", f"Registration failed: {error_detail}")
        except requests.RequestException as e:
            self.show_message("Network Error", f"Error: {str(e)}")
