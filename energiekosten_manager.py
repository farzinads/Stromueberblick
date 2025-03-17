from base import tk, ttk, messagebox, DateEntry, os

class EnergiekostenManager:
    def __init__(self, app):
        self.root = app.root
        self.app = app
        self.data = app.data
        self.current_contract = app.current_contract
        self.energiekosten_tab = app.energiekosten_tab
        self.setup_energiekosten_tab()

    def setup_energiekosten_tab(self):
        energiekosten_frame = ttk.Frame(self.energiekosten_tab)
        energiekosten_frame.place(x=10, y=10)

        ttk.Label(energiekosten_frame, text="Datum:").grid(row=0, column=0, pady=5, sticky="w")
        self.datum = DateEntry(energiekosten_frame, date_pattern="dd.mm.yyyy")
        self.datum.grid(row=0, column=1, pady=5)

        ttk.Label(energiekosten_frame, text="Kosten (€):").grid(row=1, column=0, pady=5, sticky="w")
        self.kosten = ttk.Entry(energiekosten_frame)
        self.kosten.grid(row=1, column=1, pady=5)

        ttk.Button(energiekosten_frame, text="Speichern", command=self.save_energiekosten).grid(row=2, column=0, columnspan=2, pady=10)

        table_frame = ttk.Frame(self.energiekosten_tab, relief="solid", borderwidth=2)
        table_frame.place(x=10, y=110, width=960, height=540)

        self.energiekosten_table = ttk.Treeview(table_frame, columns=("Datum", "Kosten"), show="headings", selectmode="extended")  # انتخاب چند سطر
        self.energiekosten_table.heading("Datum", text="Datum")
        self.energiekosten_table.heading("Kosten", text="Kosten (€)")
        self.energiekosten_table.column("Datum", width=150, anchor="center")
        self.energiekosten_table.column("Kosten", width=150, anchor="center")
        self.energiekosten_table.pack(fill="both", expand=True)

        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Anenden zur Rechnung", command=self.anenden_zur_rechnung)
        self.energiekosten_table.bind("<Button-3>", self.show_context_menu)

        self.update_energiekosten_table()

    def save_energiekosten(self):
        if not self.current_contract:
            messagebox.showerror("Fehler", "Kein Vertrag ausgewählt!")
            return
        datum = self.datum.get()
        kosten = self.kosten.get()
        if not all([datum, kosten]):
            messagebox.showerror("Fehler", "Datum und Kosten müssen ausgefüllت sein!")
            return
        try:
            kosten = float(kosten)
        except ValueError:
            messagebox.showerror("Fehler", "Kosten muss numerisch sein!")
            return
        energiekosten = {"vertragskonto": self.current_contract, "datum": datum, "kosten": kosten}
        if "energiekosten" not in self.data:
            self.data["energiekosten"] = []
        self.data["energiekosten"].append(energiekosten)
        self.app.save_data()
        messagebox.showinfo("Erfolg", "Energiekosten wurde gespeichert!")
        self.clear_energiekosten_entries()
        self.update_energiekosten_table()

    def update_energiekosten_table(self):
        self.current_contract = self.app.current_contract
        self.energiekosten_table.delete(*self.energiekosten_table.get_children())
        if self.current_contract and "energiekosten" in self.data:
            for ek in self.data["energiekosten"]:
                if ek["vertragskonto"] == self.current_contract:
                    self.energiekosten_table.insert("", "end", values=(ek["datum"], ek["kosten"]))

    def clear_energiekosten_entries(self):
        self.datum.delete(0, tk.END)
        self.kosten.delete(0, tk.END)

    def show_context_menu(self, event):
        row = self.energiekosten_table.identify_row(event.y)
        if row:
            self.context_menu.post(event.x_root, event.y_root)

    def anenden_zur_rechnung(self):
        selected = self.energiekosten_table.selection()
        if not selected:
            messagebox.showwarning("Warnung", "Bitte mindestens eine Zeile auswählen!")
            return
        total_kosten = 0
        datums = []
        for item in selected:
            values = self.energiekosten_table.item(item, "values")
            datums.append(values[0])
            total_kosten += float(values[1])
        
        rechnung = {
            "vertragskonto": self.current_contract,
            "rechnungsnummer": f"R{len(self.data.get('rechnungen', [])) + 1}",
            "datum": datums[-1],  # آخرین تاریخ انتخاب‌شده
            "betrag": total_kosten
        }
        if "rechnungen" not in self.data:
            self.data["rechnungen"] = []
        self.data["rechnungen"].append(rechnung)
        self.app.save_data()
        messagebox.showinfo("Erfolg", "Energiekosten wurden zur Rechnung anenden!")
        self.update_energiekosten_table()