from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.menu import MDDropdownMenu
from kivy.utils import get_color_from_hex
from kivy.app import App
import requests
from kivy_app.utils import DialogMixin
from datetime import datetime

class AddBudgetScreen(MDScreen, DialogMixin):
    selected_month = None  # Store the selected month as formatter string (YYYY-MM)
    selected_category = None  # Store the selected category

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.categories = ["Food", "Transport", "Entertainment", "Health", "Utilities", "Shopping", "Education", "Personal Care", "Travel"]
        self.category_menu = None

    def show_calendar(self):
        # Open the calendar
        calendar = MDDatePicker()
        calendar.bind(on_save=self.on_month_selected, on_cancel=self.on_calendar_cancel)
        calendar.open()

    def on_month_selected(self, instance, value, date_range):
        # Format the selected date to YYYY-MM
        self.selected_month = value.strftime("%Y-%m")
        self.ids.month_input.text = self.selected_month

    def on_calendar_cancel(self, instance, value):
        self.selected_month = None

    def show_category_menu(self):
        # Create the dropdown menu for categories
        menu_items = [
            {
                "text": category,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=category: self.set_category(x),
            } for category in self.categories
        ]
        self.category_menu = MDDropdownMenu(
            caller=self.ids.category_button,
            items=menu_items,
            width_mult=4,
        )
        self.category_menu.open()

    def set_category(self, category):
        # Set the selected category and update the button text
        self.selected_category = category
        self.ids.category_button.text = category
        self.category_menu.dismiss()

    def add_budget(self, limit):
        if not self.selected_category:
            self.show_message("Error", "Please select a category")
            return

        url = "http://127.0.0.1:6000/budgets/"
        payload = {
            "category": self.selected_category.strip(),
            "limit": float(limit),
        }

        # Add month only if provided
        if self.selected_month:
            payload["month"] = self.selected_month
        headers = {"Authorization": f"Bearer {self.manager.access_token}"}
        
        try:
            response = requests.post(url=url, headers=headers, json=payload)
            if response.status_code == 200:
                self.show_message("Success", "New budget added!")
                self.manager.current = "view_budgets"
            else:
                error_detail = response.json().get("detail", "Failed to add budget")
                self.show_message(f"Error {response.status_code}", f"Error: {error_detail}")
        except Exception as e:
            self.show_message("Network Error", f"{str(e)}")


class ViewBudgetScreen(MDScreen, DialogMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.selected_view = "current"  # Default view mode

    def on_enter(self):
        self.load_budgets()

    def load_budgets(self):
        url = "http://127.0.0.1:6000/budgets/"
        headers = {"Authorization": f"Bearer {self.manager.access_token}"}
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                budgets = response.json()
                self.display_budget_cards(budgets)
            elif response.status_code == 404:
                self.display_budget_cards([])
                self.show_message("No budgets", "You have not set any budgets. Please create one.")
            else:
                self.show_message("Error", f"Failed to load budgets {response.status_code}")
        except Exception as e:
            self.show_message("Network Error", f"Error: {str(e)}")

    def display_budget_cards(self, budgets):
        container = self.ids.budget_container
        container.clear_widgets()

        # Get the current month in YYYY-MM format
        current_month = datetime.now().strftime("%Y-%m")

        # Filter budgets based on selected view mode
        if self.selected_view == "current":
            budgets = [b for b in budgets if b["month"] == current_month]
        elif self.selected_view == "past":
            budgets = [b for b in budgets if b["month"] < current_month]
        elif self.selected_view == "future":
            budgets = [b for b in budgets if b["month"] > current_month]

        # Add "Add Budget" card
        add_budget_card = MDCard(
            orientation="vertical",
            padding="12dp",
            size_hint=(None, None),
            size=("280dp", "180dp"),
            md_bg_color=get_color_from_hex("#E0F7FA"),
            on_release=self.go_to_add_budget
        )
        add_budget_card.add_widget(MDIconButton(
            icon="plus",
            user_font_size="48sp",
            pos_hint={"center_x": 0.5}
        ))
        add_budget_card.add_widget(MDLabel(
            text="Add Budget",
            font_style="H6",
            halign="center",
            theme_text_color="Primary"
        ))
        container.add_widget(add_budget_card)

        # Add filtered budget cards
        for budget in budgets:
            card = BudgetCard(
                category=budget["category"],
                limit=budget["limit"],
                current_total=budget["current_total"],
                month=budget["month"]
            )
            container.add_widget(card)

                # Toggle Card to switch views
        toggle_card = MDCard(
            orientation="vertical",
            padding="12dp",
            size_hint=(None, None),
            size=("280dp", "80dp"),
            md_bg_color=get_color_from_hex("#E0F7FA"),
            on_release=self.toggle_view
        )
        toggle_card.add_widget(MDLabel(
            text=f"Viewing: {self.selected_view.capitalize()} Budgets",
            font_style="H6",
            halign="center",
            theme_text_color="Primary"
        ))
        container.add_widget(toggle_card)
        

    def toggle_view(self, *args):
        """Toggle between current, past, and future budgets."""
        views = ["current", "past", "future"]
        current_index = views.index(self.selected_view)
        self.selected_view = views[(current_index + 1) % len(views)]
        self.load_budgets()  # Reload budgets with the new filter

    def go_to_add_budget(self, *args):
        self.manager.current = "add_budget"


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
            response = requests.put(url=url, headers=headers, json=payload)

            if response.status_code == 200:
                response_data = response.json()
                # print("API Response:", response_data)  # Debugging

                # Extract warning and success message
                warning = response_data.get("warning")
                success_message = response_data.get("message", "Budget updated successfully.")

                # Show warning first, if present
                if warning:
                    self.show_message("Warning", warning)

                # Show success message after warning
                self.show_message("Success", success_message)
                self.manager.current = "view_budgets"

            else:
                # Handle API errors
                error_detail = response.json().get('detail', "Budget not found")
                self.show_message("Error", f"Error: {error_detail}")

        except Exception as e:
            # Handle unexpected errors
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