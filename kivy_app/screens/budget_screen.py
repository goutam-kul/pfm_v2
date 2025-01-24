from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.button import MDRaisedButton
from kivy.utils import get_color_from_hex
from kivy.app import App
import requests
from kivy_app.utils import DialogMixin

class ViewBudgetScreen(MDScreen, DialogMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_enter(self):
        self.load_budgets()

    def load_budgets(self):
        url = "http://127.0.0.1:6000/budgets/"  # Replace with your API endpoint
        headers = {"Authorization": f"Bearer {self.manager.access_token}"}
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                budgets = response.json()
                self.display_budget_cards(budgets)
            else:
                self.show_message("Error", f"Failed to load budget {response.status_code}")
        except Exception as e:
            self.show_message("Network Error", f"Error: {(str(e))}")

    def display_budget_cards(self, budgets):
        container = self.ids.budget_container
        container.clear_widgets()

        for budget in budgets:
            card = BudgetCard(
                category=budget["category"],
                limit=budget["limit"],
                current_total=budget["current_total"],
                month=budget["month"]
            )
            container.add_widget(card)


class UpdateBudgetScreen(MDScreen, DialogMixin):
    budget_month = None   # Store the month for the selected budget

    def update_budget(self, category, new_limit):
        url = "http://127.0.0.1:6000/budgets/update_budget"
        payload = {
            "category": category,
            "month": self.budget_month,
            "new_limit": float(new_limit)
        }
        headers = {"Authorization": f"Bearer {self.manager.access_token}"}
        
        try: 
            respone = requests.put(url=url, headers=headers, json=payload)
            if respone.status_code == 200:
                self.show_message("Suceess", "Budget Updated successfully.")
                self.manager.current = "view_budgets"
            else:
                error_detail = respone.json().get('detail', "Budget not found")
                self.show_message("Error", f"Error: {error_detail}")
        except Exception as e:
            self.show_message("Network Error", f"{str(e)}")


class BudgetCard(MDCard):
    def __init__(self, category, limit, current_total, month, **kwargs):
        super().__init__(**kwargs)
        self.category = category
        self.limit = limit
        self.current_total = current_total
        self.month = month
        
        self.orientation = "vertical"
        self.padding = "12dp"
        self.spacing = "8dp"
        self.size_hint = None, None
        self.size = "280dp", "180dp"
        self.md_bg_color = self.get_card_color()

        self.add_widget(MDLabel(
            text=f"Category: {category}",
            font_style="H6",
            theme_text_color="Primary"
        ))
        self.add_widget(MDLabel(
            text=f"Limit: ₹{limit:.2f}",
            font_style="Subtitle2",
            theme_text_color="Secondary"
        ))
        self.add_widget(MDLabel(
            text=f"Current: ₹{current_total:.2f}",
            font_style="Body2",
            theme_text_color="Hint"
        ))
        self.add_widget(MDLabel(
            text=f"Month: {month}",
            font_style="Caption",
            theme_text_color="Hint"
        ))
        # Calculate progress value
        progress_value = (current_total / limit) * 100 if limit > 0 else 0

        # Dynamic color calculation
        progress_color = self.calculate_color(progress_value=progress_value)

        progress = MDProgressBar(
            value=progress_value,
            color=progress_color
        )
        self.add_widget(progress)

        # Update Budget Button
        update_button = MDRaisedButton(
            text="Update Budget",
            size_hint=(0.8, None),
            height="40dp",
            pos_hint={"center_x": 0.5},
            on_release=self.go_to_update_budget
        )
        self.add_widget(update_button)

    def go_to_update_budget(self, *args):
        # Access the ScreenManager directly from the app instance
        app = App.get_running_app()
        screen_manager = app.root

        # Get the UpdateBudgetScreen and prefill the fields
        update_screen = screen_manager.get_screen("update_budget")
        update_screen.ids.category_input.text = self.category
        update_screen.ids.limit_input.text = str(self.limit)
        update_screen.budget_month = self.month  # Pass the month for later use
        screen_manager.current = "update_budget"

    def calculate_color(self, progress_value):
        """Calculates the progress bar color dynamically."""
        green = max(0, 1 - progress_value / 100)  # Green decreass as progress increase
        red = min(1, progress_value / 100)        # Red increases as progress increases
        return (red, green, 0, 1)  # RGBA format
    
    def get_card_color(self):
        """Dynamically asign a card color."""
        color_palette = [
            "#F3E5F5",  # Soft Lavender
            "#E0F7FA",  # Pastel Mint
            "#BBDEFB",  # Powder Blue
            "#FFE0B2",  # Light Peach
            "#FFF9E6",  # Soft Beige
            "#FFCCBC",  # Muted Coral
        ]
        # Alternate color based on category hash
        color_index = hash(self.category) % len(color_palette)
        return get_color_from_hex(color_palette[color_index])