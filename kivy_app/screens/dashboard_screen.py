import requests
from kivymd.uix.screen import MDScreen
import webbrowser
from kivy_app.utils import DialogMixin

class DashboardScreen(MDScreen, DialogMixin):
    def open_streamlit_dashboard(self):
        try:

            access_token = self.manager.access_token
            headers = {"Authorization": f"Bearer {access_token}"}
            url = "http://127.0.0.1:6000/users/user_id"

            response = requests.get(url=url, headers=headers)
            if response.status_code == 200:
                user_id = response.json().get("user_id")

                # Open the Streamlit dashboard in the default web browser
                streamlit_url = f"http://localhost:8501?user_id={user_id}"  
                webbrowser.open(streamlit_url)
            else:
                error_detail = response.json().get("detail", "Failed to retrieve user id")
                self.show_message("Error", f"Error:{str(error_detail)}")
        except Exception as e:
            self.show_message("Network Error", f"Error: {str(e)}")