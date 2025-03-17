<<<<<<< HEAD
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
=======
from base import tk, ttk, DateEntry

class DetailsTabs:
    def setup_contract_details_page(self):
        self.contract_details_title = ttk.Label(self.contract_details_frame, text="Vertragskontonummer: ", font=("Arial", 14, "bold"))
        self.contract_details_title.place(x=10, y=5)

        self.back_to_input_button = ttk.Button(self.contract_details_frame, text="Zurück", command=lambda: self.switch_page(self.contract_frame), style="Custom.TButton", width=10)
        self.back_to_input_button.place(x=975, y=5, anchor="ne")

        self.details_tabs = ttk.Notebook(self.contract_details_frame)
        self.tarifedaten_tab = ttk.Frame(self.details_tabs)
        self.ablesung_tab = ttk.Frame(self.details_tabs)
        self.verbrauchsmengen_tab = ttk.Frame(self.details_tabs)
        self.energiekosten_tab = ttk.Frame(self.details_tabs)
        self.zahlungen_tab = ttk.Frame(self.details_tabs)
        self.rechnungen_tab = ttk.Frame(self.details_tabs)  # تب جدید

        # اضافه کردن تب‌ها به نوت‌بوک با ترتیب درست
        self.details_tabs.add(self.tarifedaten_tab, text="Tarifedaten")
        self.details_tabs.add(self.ablesung_tab, text="Ablesung")
        self.details_tabs.add(self.verbrauchsmengen_tab, text="Verbrauchsmengen")
        self.details_tabs.add(self.energiekosten_tab, text="Energiekosten")
        self.details_tabs.add(self.zahlungen_tab, text="Zahlungen")  # بعد از Energiekosten
        self.details_tabs.add(self.rechnungen_tab, text="Rechnungen")  # بعد از Zahlungen
        
        self.details_tabs.place(x=10, y=40, width=980, height=650)
>>>>>>> 1b51e8c33d9a0d94737b7d340c7f90a601d0c100
