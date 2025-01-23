from kivymd.uix.screen import MDScreen
from kivy_app.utils import DialogMixin
from kivy.clock import Clock
import requests

class ResetPasswordScreen(MDScreen, DialogMixin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None  # Initialize the dialog attribute

    def reset_password(self, otp, new_password, confirm_password):
        # Validate that passwords match
        if new_password != confirm_password:
            self.show_message("Error", "Passwords do not match.")
            return

        url = "http://127.0.0.1:6000/users/reset-password"  # Replace with your actual endpoint
        payload = {
            "otp": otp.strip(),
            "new_password": new_password.strip(),
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                self.show_message("Success", "Password reset successful! Redirecting to log in...")
                # Schedule redirection to the login screen after 5 seconds
                Clock.schedule_once(self.redirect_to_login, 5)

            elif response.status_code == 400:
                self.show_message("Error", "OTP incorrect or expired.")
            else:
                self.show_message("Error", "Unable to reset password.")
        except Exception as e:
            self.show_message("Network Error", f"Error: {str(e)}")

    def redirect_to_login(self, dt):
        self.manager.current = "home"
