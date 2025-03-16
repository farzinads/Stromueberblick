from base import tk, ttk, messagebox, DateEntry, os

class DetailsTabs:
    def __init__(self, app):
        self.root = app.root
        self.app = app
        self.data = app.data
        self.current_contract = app.current_contract
        self.details_tab = app.details_tab  # تغییر به details_tab
        self.setup_details_tabs()

    def setup_details_tabs(self):
        details_frame = ttk.Frame(self.details_tab)
        details_frame.pack(fill="both", expand=True)

        ttk.Label(details_frame, text=f"Details für Vertrag: {self.current_contract or 'Kein Vertrag ausgewählt'}").pack(pady=10)
        # اینجا می‌تونی محتوای دلخواه رو اضافه کنی