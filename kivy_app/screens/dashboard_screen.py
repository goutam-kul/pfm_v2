import os
import time
import subprocess
import requests
from kivymd.uix.screen import MDScreen
import webbrowser
from kivy_app.utils import DialogMixin

class DashboardScreen(MDScreen, DialogMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.streamlit_process = None

    def open_streamlit_dashboard(self):
        try:
            if not self.streamlit_process or self.streamlit_process.poll() is not None:
                self.start_streamlit_server()
            
            # Wait a bit to ensure the server is ready
            time.sleep(2)
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

    def start_streamlit_server(self):
        if self.streamlit_process and self.streamlit_process.poll() is None:
            print("Streamlit server is already running")
            return 

        # Command to start the streamlit app
        streamlit_app_path = os.path.abspath("kivy_app/streamlit_dashboard.py")
        command = ["streamlit", "run", streamlit_app_path]

        # Start the streamlit server as a background process
        self.streamlit_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Streamlit server started")

    def on_leave(self):
        # Stop the streamlit server when leaving the dashboard 
        if self.streamlit_process and self.streamlit_process.poll() is None:
            self.streamlit_process.terminate()
            print("Streamlit server stopped")