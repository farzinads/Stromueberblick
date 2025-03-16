from base import tk, ttk, messagebox, save_data, os

class RechnungenManager:
    def __init__(self, app):
        self.root = app.root
        self.data = app.data
        self.current_contract = app.current_contract
        self.rechnungen_tab = app.rechnungen_tab
        self.setup_rechnungen_tab()

    def setup_rechnungen_tab(self):
        rechnungen_frame = ttk.Frame(self.rechnungen_tab)
        rechnungen_frame.place(x=10, y=10)

        ttk.Label(rechnungen_frame, text="Rechnungsnummer:").grid(row=0, column=0, pady=5, sticky="w")
        self.rechnungsnummer = ttk.Entry(rechnungen_frame)
        self.rechnungsnummer.grid(row=0, column=1, pady=5)

        table_frame_rechnungen = ttk.Frame(self.rechnungen_tab, relief="solid", borderwidth=2)
        table_frame_rechnungen.place(x=10, y=60, width=960, height=590)

        self.rechnungen_table = ttk.Treeview(table_frame_rechnungen, columns=("Rechnungsnummer", "Datum", "Betrag"), show="headings")
        self.rechnungen_table.heading("Rechnungsnummer", text="Rechnungsnummer")
        self.rechnungen_table.heading("Datum", text="Datum")
        self.rechnungen_table.heading("Betrag", text="Betrag (€)")
        self.rechnungen_table.column("Rechnungsnummer", width=200, anchor="center")
        self.rechnungen_table.column("Datum", width=150, anchor="center")
        self.rechnungen_table.column("Betrag", width=150, anchor="center")

        scrollbar_rechnungen = ttk.Scrollbar(table_frame_rechnungen, orient="vertical", command=self.rechnungen_table.yview)
        self.rechnungen_table.configure(yscrollcommand=scrollbar_rechnungen.set)
        scrollbar_rechnungen.pack(side="right", fill="y")
        self.rechnungen_table.pack(fill="both", expand=True)

        self.update_rechnungen_table()

    def update_rechnungen_table(self):
        self.rechnungen_table.delete(*self.rechnungen_table.get_children())
        if self.current_contract and "rechnungen" in self.data:
            for item in self.data["rechnungen"]:
                if item["vertragskonto"] == self.current_contract:
                    self.rechnungen_table.insert("", "end", values=(item["rechnungsnummer"], item["datum"], item["betrag"]))