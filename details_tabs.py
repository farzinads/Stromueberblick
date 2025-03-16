from base import tk, ttk

class DetailsTabs:
    def __init__(self, app):
        self.root = app.root
        self.data = app.data
        self.current_contract = app.current_contract
        self.details_tab = app.details_tab
        self.setup_details_tabs()

    def setup_details_tabs(self):
        details_notebook = ttk.Notebook(self.details_tab)
        details_notebook.pack(fill="both", expand=True)

        self.verbrauchsmengen_tab = ttk.Frame(details_notebook)
        self.rechnungen_tab = ttk.Frame(details_notebook)
        self.zahlungen_tab = ttk.Frame(details_notebook)

        details_notebook.add(self.verbrauchsmengen_tab, text="Verbrauchsmengen")
        details_notebook.add(self.rechnungen_tab, text="Rechnungen")
        details_notebook.add(self.zahlungen_tab, text="Zahlungen")

        self.create_verbrauchsmengen_tab()
        self.create_rechnungen_tab()
        self.create_zahlungen_tab()

    def create_verbrauchsmengen_tab(self):
        tk.Label(self.verbrauchsmengen_tab, text="Verbrauchsmengen Details").pack(pady=10)

    def create_rechnungen_tab(self):
        tk.Label(self.rechnungen_tab, text="Rechnungen Details").pack(pady=10)

    def create_zahlungen_tab(self):
        tk.Label(self.zahlungen_tab, text="Zahlungen Details").pack(pady=10)