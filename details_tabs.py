from base import tk, ttk, messagebox, DateEntry, os

class DetailsTabs:
    def __init__(self, app):
        self.root = app.root
        self.app = app
        self.data = app.data
        self.current_contract = app.current_contract
        self.details_tab = app.details_tab
        self.setup_details_tabs()

    def setup_details_tabs(self):
        details_frame = ttk.Frame(self.details_tab)
        details_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Label(details_frame, text=f"Details für Vertrag: {self.current_contract or 'Kein Vertrag ausgewählt'}", font=("Arial", 12, "bold")).pack(pady=10)

        # جدول اطلاعات قرارداد
        table_frame = ttk.Frame(details_frame, relief="solid", borderwidth=2)
        table_frame.pack(fill="both", expand=True)

        self.details_table = ttk.Treeview(table_frame, columns=("Feld", "Wert"), show="headings")
        self.details_table.heading("Feld", text="Feld")
        self.details_table.heading("Wert", text="Wert")
        self.details_table.column("Feld", width=200, anchor="w")
        self.details_table.column("Wert", width=400, anchor="w")
        self.details_table.pack(fill="both", expand=True)

        self.update_details()

    def update_details(self):
        self.details_table.delete(*self.details_table.get_children())
        if self.current_contract:
            for contract in self.data["contracts"]:
                if contract["vertragskonto"] == self.current_contract:
                    fields = [
                        ("Anbieter", contract.get("company", "-")),
                        ("Anschrift", contract.get("company_address", "-")),
                        ("Telefonnummer", contract.get("phone", "-")),
                        ("E-Mail", contract.get("email", "-")),
                        ("Vertragskontonummer", contract.get("vertragskonto", "-")),
                        ("Zählernummer", contract.get("zählernummer", "-")),
                        ("Vertragsbeginn", contract.get("start_date", "-")),
                        ("Vertragstyp", contract.get("contract_type", "-"))
                    ]
                    for field, value in fields:
                        self.details_table.insert("", "end", values=(field, value))
                    break