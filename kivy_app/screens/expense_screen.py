from kivymd.uix.screen import MDScreen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy_app.utils import DialogMixin
import requests


class ExpenseMainScreen(MDScreen):
    pass


class AddExpenseScreen(MDScreen, DialogMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dialog = None

    def add_expense(self, category, amount, date):
        url = "http://127.0.0.1:6000/expenses/"
        payload = {
            "category": category,
            "amount": float(amount),
            "date": date
        }
        headers = {
            "Authorization": f"Bearer {self.manager.access_token}"
        }
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                self.manager.current = "expense_main"
            else:
                self.show_message("Error", "Expense addition failed succesfully.")
        except Exception as e:
            self.show_message("Network Error", f"Error: {str(e)}")


class ViewExpensesScreen(MDScreen, DialogMixin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.expense_table = None
        self.create_table()
        self.dialog = None

    def create_table(self):
        # Define the MDDataTable with larger size and more rows per page
        self.expense_table = MDDataTable(
            size_hint=(1, 1),  # Larger table with 90% width and 80% height
            use_pagination=True,
            rows_num=15,  # Number of entries per page
            column_data=[
                ("Date", dp(50)),
                ("Category", dp(50)),
                ("Amount", dp(50)),
            ],
            row_data=[],  # Initially empty, populated dynamically
            elevation=2,
        )
        # Add the table to the table_container
        self.ids.table_container.add_widget(self.expense_table)

    def populate_table(self):
        url = "http://127.0.0.1:6000/expenses/"
        headers = {
            "Authorization": f"Bearer {self.manager.access_token}"
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                expenses = response.json()
                table_data = [
                    (expense["date"], expense["category"], str(expense["amount"]))
                    for expense in expenses
                ]
                self.expense_table.row_data = table_data  # Populate table with rows
            elif response.status_code == 404:
                self.show_message("Error", "Expenses not found.")
            else:
                error_detail = response.json().get("detail", "Unknown error")
                self.show_message("Unknown Error", f"Error: {response.status_code} - {error_detail}")
        except Exception as e:
            self.show_message("Network Error", f"Error: {str(e)}")

    def on_enter(self):
        # Populate the table when the screen is entered
        self.populate_table()
