from kivy.uix.screenmanager import Screen
import requests

class HomeScreen(Screen):
    def login_user(self, identifier, password):
        url = "http://127.0.0.1:6000/users/login"  # Login endpoint
        payload = {"identifier": identifier, "password": password}
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                access_token = data.get("access_token")
                token_type = data.get("token_type")
                if access_token:
                    # Save the token for authentication API calls (e.g., in a global variable or secure storage)
                    self.manager.access_token = access_token
                    self.manager.token_type = token_type
                    self.manager.current = "dashboard"  # Navigate to dashboard
                else:
                    self.ids.status_lable.text = "Login failed: No token received"
            else:
                # Handle API error:
                error_detail = response.json().get("detail", "Unknown error")
                if "User Not Found" in error_detail:
                    self.ids.status_label.text = "Error: User not found. Please check your username or email and try again."
                elif "Invalid Password" in error_detail:
                    self.ids.status_label.text = "Error: Incorrect password. Please try again."
                else:
                    self.ids.status_lable.text = f"Error: {error_detail}"
        except Exception as e:
            self.ids.status_label.text = f"Error: {e}"

    def register_user(self, username, password, email):
        url = "http://127.0.0.1:6000/users/register"  # Register endpoint
        payload = {
            "username": username,
            "email": email,
            "password": password
        }
        try:
            response = requests.post(url=url, json=payload)
            if response.status_code == 200:
                self.ids.status_label.text = "Registration successful! Please log in using your username/email and password."
            else:
                self.ids.status_lable.text = "Registration failed: " + response.json().get('detail', 'Unknown error')
        except Exception as e:
            self.ids.status_label.text = f"Error: {e}"

    def forgot_password(self, email):
        url = "http://127.0.0.1:6000/users/forgot-password"  # Forgot password endpoint
        payload = {"email": email}
        try: 
            response = requests.post(url=url, json=payload)
            if response.status_code == 200:
                self.ids.status_label.text = "A password reset link has been sent to your email."
            else:
                self.ids.status_label.text = "Error: " + response.json().get('detail', 'Unknown error')
        except Exception as e:
            self.ids.status_label.text = f"Error: {e}"