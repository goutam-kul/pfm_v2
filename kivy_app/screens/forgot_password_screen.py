from kivy.uix.screenmanager import Screen
import requests

class ForgotPasswordScreen(Screen):
    def send_reset_link(self, email):
        email = email.strip()  # Remove whitespace
        print(f"Email entered: {email}")  # Debugging
        url = "http://127.0.0.1:6000/users/forgot-password"
        payload = {"email": email}
        try:
            response = requests.post(url, json=payload)
            print(response.json())  # Debugging
            if response.status_code == 200:
                self.ids.status_label.text = "Reset link sent to your email."
                # Store email in the screen manager to pass to the Reset Password screen
                self.manager.email = email
                # Navigate to Reset Password screen
                self.manager.current = "reset_password"
            elif response.status_code == 404:
                error_detail = response.json().get("detail", "Email not registered.")
                self.ids.status_label.text = f"Error: {error_detail}"
            else:
                self.ids.status_label.text = "Error: Unable to send reset link."
        except Exception as e:
            self.ids.status_label.text = f"Error: {str(e)}"
