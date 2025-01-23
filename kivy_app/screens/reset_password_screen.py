from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
import requests

class ResetPasswordScreen(Screen):
    def reset_password(self, otp, new_password):
        url = "http://127.0.0.1:6000/users/reset-password"  # Replace with your actual endpoint
        payload = {
            "otp": otp.strip(),
            "new_password": new_password.strip(),
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                self.ids.status_label.text = "Password reset successful! Redirecting to log in..."
                # CHedule redirection to the login screen after 5 seconds 
                Clock.schedule_once(self.redirect_to_login, 5)

            elif response.status_code == 400:
                self.ids.status_label.text = "Error: OTP incorrect or expired."
            else:
                self.ids.status_label.text = "Error: Unable to reset password."
        except Exception as e:
            self.ids.status_label.text = f"Error: {str(e)}"

    def redirect_to_login(self, dt):
        self.manager.current = "home"