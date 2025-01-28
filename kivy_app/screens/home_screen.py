from kivymd.uix.screen import MDScreen
from kivy_app.utils import DialogMixin
import requests

class HomeScreen(MDScreen, DialogMixin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "home"
        self.dialog = None
        
    def login_user(self, identifier, password):
        url = "http://127.0.0.1:6000/users/login"
        payload = {"identifier": identifier.strip(), "password": password.strip()}
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                access_token = data.get("access_token")
                token_type = data.get("token_type")
                if access_token:
                    self.manager.access_token = access_token
                    self.manager.token_type = token_type
                    self.manager.current = "dashboard"
                else:
                    self.show_message("Error", "Login failed: No token received")
            else:
                error_detail = response.json().get("detail", "Unknown error")
                self.show_message("Error", f"Login Failed: {error_detail}")
        except requests.RequestException as e:
            self.show_message("Network error", f"Error: {str(e)}")

    def logout_user(self):
        # Clear fields and naviagate to the home screen
        self.clear_fields()
        self.manager.current = "home"

    def clear_fields(self):
        self.ids.identifier.text = ""
        self.ids.password.text = ""