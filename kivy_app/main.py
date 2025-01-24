from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder

from kivy_app.screens.expense_screen import (
    ExpenseMainScreen,
    AddExpenseScreen,
    ViewExpensesScreen
)
from kivy_app.screens.budget_screen import (
    # AddBudgetScreen,
    ViewBudgetScreen,
    UpdateBudgetScreen
)
from kivy_app.screens.dashboard_screen import DashboardScreen
from kivy_app.screens.home_screen import HomeScreen
from kivy_app.screens.register_screen import RegisterScreen
from kivy_app.screens.forgot_password_screen import ForgotPasswordScreen
from kivy_app.screens.reset_password_screen import ResetPasswordScreen


# Load .kv files
Builder.load_file("kivy_app/kivy/home_screen.kv")
Builder.load_file("kivy_app/kivy/dashboard_screen.kv")
Builder.load_file("kivy_app/kivy/register_screen.kv")
Builder.load_file("kivy_app/kivy/forgot_password_screen.kv")
Builder.load_file("kivy_app/kivy/reset_password_screen.kv")
Builder.load_file("kivy_app/kivy/expense_screen.kv")
Builder.load_file("kivy_app/kivy/budget_screen.kv")

class FinanceManagerApp(MDApp):
    def build(self):
        sm = ScreenManager()

        # Add add screens to the screen manager
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(ForgotPasswordScreen(name="forgot_password"))
        sm.add_widget(ResetPasswordScreen(name="reset_password"))
        sm.add_widget(DashboardScreen(name="dashboard"))
        # Expenses screens
        sm.add_widget(ExpenseMainScreen(name="expense_main"))
        sm.add_widget(AddExpenseScreen(name="add_expense"))
        sm.add_widget(ViewExpensesScreen(name="view_expenses"))
        # Budget screens
        # sm.add_widget(AddBudgetScreen(name="add_budget"))
        sm.add_widget(ViewBudgetScreen(name="view_budgets"))
        sm.add_widget(UpdateBudgetScreen(name="update_budget"))
        return sm
    

if __name__ == "__main__":
    FinanceManagerApp().run()