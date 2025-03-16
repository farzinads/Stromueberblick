from base import tk, ttk, messagebox, DateEntry, os

class ZahlungManager:
    def __init__(self, app):
        self.root = app.root
        self.app = app
        self.data = app.data
        self.current_contract = app.current_contract
        self.zahlung_tab = app.zahlungen_tab  # تغییر به zahlungen_tab
        self.setup_zahlung_tab()

    def setup_zahlung_tab(self):
        zahlung_frame = ttk.Frame(self.zahlung_tab)
        zahlung_frame.place(x=10, y=10)

        ttk.Label(zahlung_frame, text="Datum:").grid(row=0, column=0, pady=5, sticky="w")
        self.datum = DateEntry(zahlung_frame, date_pattern="dd.mm.yyyy")
        self.datum.grid(row=0, column=1, pady=5)

        ttk.Label(zahlung_frame, text="Betrag (€):").grid(row=1, column=0, pady=5, sticky="w")
        self.betrag = ttk.Entry(zahlung_frame)
        self.betrag.grid(row=1, column=1, pady=5)

        ttk.Button(zahlung_frame, text="Speichern", command=self.save_zahlung).grid(row=2, column=0, columnspan=2, pady=10)

        table_frame = ttk.Frame(self.zahlung_tab, relief="solid", borderwidth=2)
        table_frame.place(x=10, y=110, width=960, height=540)

        self.zahlung_table = ttk.Treeview(table_frame, columns=("Datum", "Betrag"), show="headings")
        self.zahlung_table.heading("Datum", text="Datum")
        self.zahlung_table.heading("Betrag", text="Betrag (€)")
        self.zahlung_table.column("Datum", width=150, anchor="center")
        self.zahlung_table.column("Betrag", width=150, anchor="center")
        self.zahlung_table.pack(fill="both", expand=True)

        self.update_zahlung_table()

    def save_zahlung(self):
        if not self.current_contract:
            messagebox.showerror("Fehler", "Kein Vertrag ausgewählt!")
            return
        datum = self.datum.get()
        betrag = self.betrag.get()
        if not all([datum, betrag]):
            messagebox.showerror("Fehler", "Datum und Betrag müssen ausgefüllت sein!")
            return
        try:
            betrag = float(betrag)
        except ValueError:
            messagebox.showerror("Fehler", "Betrag muss numerisch sein!")
            return
        zahlung = {"vertragskonto": self.current_contract, "datum": datum, "betrag": betrag}
        if "zahlungen" not in self.data:
            self.data["zahlungen"] = []
        self.data["zahlungen"].append(zahlung)
        self.app.save_data()
        messagebox.showinfo("Erfolg", "Zahlung wurde gespeichert!")
        self.clear_zahlung_entries()
        self.update_zahlung_table()

    def update_zahlung_table(self):
        self.zahlung_table.delete(*self.zahlung_table.get_children())
        if self.current_contract and "zahlungen" in self.data:
            for zahlung in self.data["zahlungen"]:
                if zahlung["vertragskonto"] == self.current_contract:
                    self.zahlung_table.insert("", "end", values=(zahlung["datum"], zahlung["betrag"]))

    def clear_zahlung_entries(self):
        self.datum.delete(0, tk.END)
        self.betrag.delete(0, tk.END)