from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.factory import Factory
from kivy_app.screens.home_screen import HomeScreen  # Import from home_screen.py
from kivy_app.screens.dashboard_screen import DashboardScreen
from kivy_app.screens.expense_screen import ExpenseScreen
from kivy_app.screens.forgot_password_screen import ForgotPasswordScreen
from kivy_app.screens.reset_password_screen import ResetPasswordScreen

# Load the .kv file explicitly
Builder.load_file("kivy_app/kivy/home.kv")
Builder.load_file("kivy_app/kivy/dashboard.kv")
Builder.load_file("kivy_app/kivy/expense.kv")
Builder.load_file("kivy_app/kivy/forgot_password.kv")
Builder.load_file("kivy_app/kivy/reset_password.kv")

# Screen Manager
class FinanceManagerApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(DashboardScreen(name="dashboard"))
        sm.add_widget(ExpenseScreen(name="expenses"))
        sm.add_widget(ForgotPasswordScreen(name="forgot_password"))
        sm.add_widget(ResetPasswordScreen(name="reset_password"))
        return sm

if __name__ == "__main__":
    FinanceManagerApp().run()
