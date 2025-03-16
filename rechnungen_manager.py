from base import tk, ttk, messagebox, DateEntry, os

class RechnungenManager:
    def __init__(self, app):
        self.root = app.root
        self.app = app
        self.data = app.data
        self.current_contract = app.current_contract
        self.rechnungen_tab = app.rechnungen_tab  # تغییر به rechnungen_tab
        self.setup_rechnungen_tab()

    def setup_rechnungen_tab(self):
        rechnungen_frame = ttk.Frame(self.rechnungen_tab)
        rechnungen_frame.place(x=10, y=10)

        ttk.Label(rechnungen_frame, text="Rechnungsnummer:").grid(row=0, column=0, pady=5, sticky="w")
        self.rechnungsnummer = ttk.Entry(rechnungen_frame)
        self.rechnungsnummer.grid(row=0, column=1, pady=5)

        ttk.Label(rechnungen_frame, text="Datum:").grid(row=1, column=0, pady=5, sticky="w")
        self.datum = DateEntry(rechnungen_frame, date_pattern="dd.mm.yyyy")
        self.datum.grid(row=1, column=1, pady=5)

        ttk.Label(rechnungen_frame, text="Betrag (€):").grid(row=2, column=0, pady=5, sticky="w")
        self.betrag = ttk.Entry(rechnungen_frame)
        self.betrag.grid(row=2, column=1, pady=5)

        ttk.Button(rechnungen_frame, text="Speichern", command=self.save_rechnung).grid(row=3, column=0, columnspan=2, pady=10)

        table_frame = ttk.Frame(self.rechnungen_tab, relief="solid", borderwidth=2)
        table_frame.place(x=10, y=110, width=960, height=540)

        self.rechnungen_table = ttk.Treeview(table_frame, columns=("Rechnungsnummer", "Datum", "Betrag"), show="headings")
        self.rechnungen_table.heading("Rechnungsnummer", text="Rechnungsnummer")
        self.rechnungen_table.heading("Datum", text="Datum")
        self.rechnungen_table.heading("Betrag", text="Betrag (€)")
        self.rechnungen_table.column("Rechnungsnummer", width=150, anchor="center")
        self.rechnungen_table.column("Datum", width=150, anchor="center")
        self.rechnungen_table.column("Betrag", width=150, anchor="center")
        self.rechnungen_table.pack(fill="both", expand=True)

        self.update_rechnungen_table()

    def save_rechnung(self):
        if not self.current_contract:
            messagebox.showerror("Fehler", "Kein Vertrag ausgewählt!")
            return
        rechnungsnummer = self.rechnungsnummer.get()
        datum = self.datum.get()
        betrag = self.betrag.get()
        if not all([rechnungsnummer, datum, betrag]):
            messagebox.showerror("Fehler", "Rechnungsnummer, Datum und Betrag müssen ausgefüllت sein!")
            return
        try:
            betrag = float(betrag)
        except ValueError:
            messagebox.showerror("Fehler", "Betrag muss numerisch sein!")
            return
        rechnung = {"vertragskonto": self.current_contract, "rechnungsnummer": rechnungsnummer, "datum": datum, "betrag": betrag}
        if "rechnungen" not in self.data:
            self.data["rechnungen"] = []
        self.data["rechnungen"].append(rechnung)
        self.app.save_data()
        messagebox.showinfo("Erfolg", "Rechnung wurde gespeichert!")
        self.clear_rechnung_entries()
        self.update_rechnungen_table()

    def update_rechnungen_table(self):
        self.rechnungen_table.delete(*self.rechnungen_table.get_children())
        if self.current_contract and "rechnungen" in self.data:
            for rechnung in self.data["rechnungen"]:
                if rechnung["vertragskonto"] == self.current_contract:
                    self.rechnungen_table.insert("", "end", values=(rechnung["rechnungsnummer"], rechnung["datum"], rechnung["betrag"]))

    def clear_rechnung_entries(self):
        self.rechnungsnummer.delete(0, tk.END)
        self.datum.delete(0, tk.END)
        self.betrag.delete(0, tk.END)