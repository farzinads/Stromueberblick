from base import tk, ttk, messagebox, DateEntry, os

class AblesungManager:
    def __init__(self, app, tab):
        self.root = app.root
        self.app = app
        self.data = app.data
        self.current_contract = app.current_contract
        self.ablesung_tab = tab
        self.setup_ablesung_tab()

    def setup_ablesung_tab(self):
        ablesung_frame = ttk.Frame(self.ablesung_tab)
        ablesung_frame.place(x=10, y=10)

        ttk.Label(ablesung_frame, text="Datum:").grid(row=0, column=0, pady=5, sticky="w")
        self.datum = DateEntry(ablesung_frame, date_pattern="dd.mm.yyyy")
        self.datum.grid(row=0, column=1, pady=5)

        ttk.Label(ablesung_frame, text="Zählerstand:").grid(row=1, column=0, pady=5, sticky="w")
        self.zählerstand = ttk.Entry(ablesung_frame)
        self.zählerstand.grid(row=1, column=1, pady=5)

        ttk.Button(ablesung_frame, text="Speichern", command=self.save_ablesung).grid(row=2, column=0, columnspan=2, pady=10)

        table_frame = ttk.Frame(self.ablesung_tab, relief="solid", borderwidth=2)
        table_frame.place(x=10, y=110, width=960, height=540)

        self.ablesung_table = ttk.Treeview(table_frame, columns=("Datum", "Zählerstand"), show="headings")
        self.ablesung_table.heading("Datum", text="Datum")
        self.ablesung_table.heading("Zählerstand", text="Zählerstand")
        self.ablesung_table.column("Datum", width=150, anchor="center")
        self.ablesung_table.column("Zählerstand", width=150, anchor="center")
        self.ablesung_table.pack(fill="both", expand=True)

        self.update_ablesung_table()

    def save_ablesung(self):
        if not self.current_contract:
            messagebox.showerror("Fehler", "Kein Vertrag ausgewählt!")
            return
        datum = self.datum.get()
        zählerstand = self.zählerstand.get()
        if not all([datum, zählerstand]):
            messagebox.showerror("Fehler", "Datum und Zählerstand müssen ausgefüllت sein!")
            return
        try:
            zählerstand = float(zählerstand)
        except ValueError:
            messagebox.showerror("Fehler", "Zählerstand muss numerisch sein!")
            return
        ablesung = {"vertragskonto": self.current_contract, "datum": datum, "zählerstand": zählerstand}
        if "ablesungen" not in self.data:
            self.data["ablesungen"] = []
        self.data["ablesungen"].append(ablesung)
        self.app.save_data()
        messagebox.showinfo("Erfolg", "Ablesung wurde gespeichert!")
        self.clear_ablesung_entries()
        self.update_ablesung_table()

    def update_ablesung_table(self):
        self.ablesung_table.delete(*self.ablesung_table.get_children())
        if self.current_contract and "ablesungen" in self.data:
            for ablesung in self.data["ablesungen"]:
                if ablesung["vertragskonto"] == self.current_contract:
                    self.ablesung_table.insert("", "end", values=(ablesung["datum"], ablesung["zählerstand"]))

    def clear_ablesung_entries(self):
        self.datum.delete(0, tk.END)
        self.zählerstand.delete(0, tk.END)