from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from collections import deque

class DialogMixin:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None  # Initialize dialog
        self.dialog_queue = deque()

    def show_message(self, title, message):
        """Adds a message to queue and displays it if no  dialog is active."""
        self.dialog_queue.append((title, message))
        if not self.dialog:
            self._show_next_dialog()

    def _show_next_dialog(self):
        if self.dialog_queue:
            title, message = self.dialog_queue.popleft()
            self.dialog = MDDialog(
                title=title,
                text=message,
                buttons=[
                    MDRaisedButton(
                        text="OK",
                        on_release=self._close_dialog  # Pass the function reference 
                    )
                ]
            )
            self.dialog.open()

    def _close_dialog(self, *args):
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None        # Reste the dialog
            self._show_next_dialog()  # Show the next dialog in the queue