from kivy.uix.screenmanager import Screen
import requests

class ExpenseScreen(Screen):
    def add_expense(self, category, amount, date):
        url = "http://127.0.0.1:6000/expenses/"  # Replace with your actual endpoint
        payload = {
            "category": category,
            "amount": float(amount),
            "date": date
        }
        headers = {
            "Authorization": f"Bearer {self.manager.access_token}"  # Access token from login
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                self.ids.status_label.text = "Expense added successfully!"
                self.clear_fields()
            elif response.status_code == 422:
                error_details = response.json().get("error", [])
                if error_details:
                    # Parse and display field-specific errors
                    error_messages = "\n".join([
                        f"{error['field']}: {error['message']}" for error in error_details
                    ])
                    self.ids.status_label.text = f"Error:\n{error_messages}"
                else:
                    self.ids.status_label.text = "Error: Unknown error occurred."
            else:
                self.ids.status_label.text = f"Error: Unexpected error occurred. {response.status_code}"
        except Exception as e:
            self.ids.status_label.text = f"Error: Unable to connect to the server. {str(e)}"


    def view_expenses(self):
        url = "http://127.0.0.1:6000/expenses/"  # Replace with your actual endpoint
        headers = {
            "Authorization": f"Bearer {self.manager.access_token}"  # Access token from login
        }

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                expenses = response.json()
                # Correctly access the individual expense details
                self.ids.status_label.text = "\n".join([
                    f"{expense['date']}: {expense['category']} - {expense['amount']}"
                    for expense in expenses
                ])
            else:
                error_detail = response.json().get("detail", "Unknown error")
                self.ids.status_label.text = f"Error: {error_detail}"
        except Exception as e:
            self.ids.status_label.text = f"Error: Unable to connect to the server. {str(e)}"


    def clear_fields(self):
        self.ids.category_input.text = ""
        self.ids.amount_input.text = ""
        self.ids.date_input.text = ""