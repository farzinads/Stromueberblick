from base import tk, ttk, messagebox, DateEntry, os

class TarifManager:
    def __init__(self, app):
        self.root = app.root
        self.data = app.data
        self.current_contract = app.current_contract
        self.tarif_tab = app.tarif_tab
        self.setup_tarif_tab()

    def setup_tarif_tab(self):
        tarif_frame = ttk.Frame(self.tarif_tab)
        tarif_frame.place(x=10, y=10)

        ttk.Label(tarif_frame, text="Tarifname:").grid(row=0, column=0, pady=5, sticky="w")
        self.tarifname = ttk.Entry(tarif_frame)
        self.tarifname.grid(row=0, column=1, pady=5)

        ttk.Label(tarif_frame, text="Preis pro kWh (€):").grid(row=1, column=0, pady=5, sticky="w")
        self.preis_pro_kwh = ttk.Entry(tarif_frame)
        self.preis_pro_kwh.grid(row=1, column=1, pady=5)

        ttk.Label(tarif_frame, text="Startdatum:").grid(row=2, column=0, pady=5, sticky="w")
        self.startdatum = DateEntry(tarif_frame, date_pattern="dd.mm.yyyy")
        self.startdatum.grid(row=2, column=1, pady=5)

        ttk.Button(tarif_frame, text="Speichern", command=self.save_tarif).grid(row=3, column=0, columnspan=2, pady=10)

        table_frame_tarif = ttk.Frame(self.tarif_tab, relief="solid", borderwidth=2)
        table_frame_tarif.place(x=10, y=110, width=960, height=540)

        self.tarif_table = ttk.Treeview(table_frame_tarif, columns=("Tarifname", "Preis pro kWh", "Startdatum"), show="headings")
        self.tarif_table.heading("Tarifname", text="Tarifname")
        self.tarif_table.heading("Preis pro kWh", text="Preis pro kWh (€)")
        self.tarif_table.heading("Startdatum", text="Startdatum")
        self.tarif_table.column("Tarifname", width=200, anchor="center")
        self.tarif_table.column("Preis pro kWh", width=150, anchor="center")
        self.tarif_table.column("Startdatum", width=150, anchor="center")

        scrollbar_tarif = ttk.Scrollbar(table_frame_tarif, orient="vertical", command=self.tarif_table.yview)
        self.tarif_table.configure(yscrollcommand=scrollbar_tarif.set)
        scrollbar_tarif.pack(side="right", fill="y")
        self.tarif_table.pack(fill="both", expand=True)

        self.update_tarif_table()

    def save_tarif(self):
        if not self.current_contract:
            messagebox.showerror("Fehler", "Kein Vertrag ausgewählt!")
            return
        tarifname = self.tarifname.get()
        preis_pro_kwh = self.preis_pro_kwh.get()
        startdatum = self.startdatum.get()
        if not all([tarifname, preis_pro_kwh, startdatum]):
            messagebox.showerror("Fehler", "Tarifname, Preis pro kWh und Startdatum müssen ausgefüllت sein!")
            return
        try:
            preis_pro_kwh = float(preis_pro_kwh)
        except ValueError:
            messagebox.showerror("Fehler", "Preis pro kWh muss numerisch sein!")
            return
        tarif = {"vertragskonto": self.current_contract, "tarifname": tarifname, "preis_pro_kwh": preis_pro_kwh, "startdatum": startdatum}
        if "tarife" not in self.data:
            self.data["tarife"] = []
        self.data["tarife"].append(tarif)
        self.app.save_data()  # تغییر به self.app.save_data()
        messagebox.showinfo("Erfolg", "Tarif wurde gespeichert!")
        self.clear_tarif_entries()
        self.update_tarif_table()

    def update_tarif_table(self):
        self.tarif_table.delete(*self.tarif_table.get_children())
        if self.current_contract and "tarife" in self.data:
            for tarif in self.data["tarife"]:
                if tarif["vertragskonto"] == self.current_contract:
                    self.tarif_table.insert("", "end", values=(tarif["tarifname"], tarif["preis_pro_kwh"], tarif["startdatum"]))

    def clear_tarif_entries(self):
        self.tarifname.delete(0, tk.END)
        self.preis_pro_kwh.delete(0, tk.END)
        self.startdatum.delete(0, tk.END)