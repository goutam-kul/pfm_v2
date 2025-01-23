from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton

class DialogMixin:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None  # Initialize dialog

    def show_message(self, title, message):
        """
        Displays a modal dialog with a message.
        """
        # Close any existing dialog
        if self.dialog:
            self.dialog.dismiss()

        # Create a new dialog
        self.dialog = MDDialog(
            title=title,
            text=message,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: self.dialog.dismiss()
                )
            ],
        )
        self.dialog.open()
