from kivymd.uix.screen import MDScreen
from kivy_app.utils import DialogMixin
import requests

class ForgotPasswordScreen(MDScreen, DialogMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dialog = None

    def send_reset_link(self, email):
        email = email.strip()  # Remove whitespace
        print(f"Email entered: {email}")  # Debugging
        url = "http://127.0.0.1:6000/users/forgot-password"
        payload = {"email": email}
        try:
            response = requests.post(url, json=payload)
            print(response.json())  # Debugging
            if response.status_code == 200:
                self.show_message("Success", "Reset link sent to your email.")
                # Store email in the screen manager to pass to the Reset Password screen
                self.manager.email = email
                # Navigate to Reset Password screen
                self.manager.current = "reset_password"
            elif response.status_code == 404:
                error_detail = response.json().get("detail", "Email not registered.")
                self.show_message("Error", f"Error: {error_detail}")
            else:
                self.show_message("Unknown Error",  "Unable to send reset link.")
        except Exception as e:
            self.show_message("Network Error", f"Error: {str(e)}")
