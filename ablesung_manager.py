from base import tk, ttk, messagebox, DateEntry, os
from datetime import datetime

class AblesungManager:
    def __init__(self, app):
        self.root = app.root
        self.data = app.data
        self.current_contract = app.current_contract
        self.ablesung_tab = app.ablesung_tab
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

        table_frame_ablesung = ttk.Frame(self.ablesung_tab, relief="solid", borderwidth=2)
        table_frame_ablesung.place(x=10, y=110, width=960, height=540)

        self.ablesung_table = ttk.Treeview(table_frame_ablesung, columns=("Datum", "Zählerstand", "Verbrauch", "Kosten"), show="headings", selectmode="extended")
        self.ablesung_table.heading("Datum", text="Datum")
        self.ablesung_table.heading("Zählerstand", text="Zählerstand")
        self.ablesung_table.heading("Verbrauch", text="Verbrauch (kWh)")
        self.ablesung_table.heading("Kosten", text="Kosten (€)")
        self.ablesung_table.column("Datum", width=150, anchor="center")
        self.ablesung_table.column("Zählerstand", width=150, anchor="center")
        self.ablesung_table.column("Verbrauch", width=150, anchor="center")
        self.ablesung_table.column("Kosten", width=150, anchor="center")

        scrollbar_ablesung = ttk.Scrollbar(table_frame_ablesung, orient="vertical", command=self.ablesung_table.yview)
        self.ablesung_table.configure(yscrollcommand=scrollbar_ablesung.set)
        scrollbar_ablesung.pack(side="right", fill="y")
        self.ablesung_table.pack(fill="both", expand=True)

        self.context_menu_ablesung = tk.Menu(self.root, tearoff=0)
        self.context_menu_ablesung.add_command(label="Senden zur Rechnung", command=self.send_to_rechnung)
        self.ablesung_table.bind("<Button-3>", self.show_context_menu_ablesung)

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
        self.data["ablesungen"] = sorted(self.data["ablesungen"], key=lambda x: datetime.strptime(x["datum"], "%d.%m.%Y"))
        self.app.save_data()  # تغییر به self.app.save_data()
        messagebox.showinfo("Erfolg", "Ablesung wurde gespeichert!")
        self.clear_ablesung_entries()
        self.update_ablesung_table()

    def update_ablesung_table(self):
        self.ablesung_table.delete(*self.ablesung_table.get_children())
        if self.current_contract and "ablesungen" in self.data:
            sorted_ablesungen = sorted([a for a in self.data["ablesungen"] if a["vertragskonto"] == self.current_contract], key=lambda x: datetime.strptime(x["datum"], "%d.%m.%Y"))
            prev_zählerstand = None
            for ablesung in sorted_ablesungen:
                verbrauch = "-"
                kosten = "-"
                if prev_zählerstand is not None:
                    verbrauch = ablesung["zählerstand"] - prev_zählerstand
                    tarif = next((t for t in self.data.get("tarife", []) if t["vertragskonto"] == self.current_contract), None)
                    kosten = verbrauch * float(tarif["preis_pro_kwh"]) if tarif and "preis_pro_kwh" in tarif else "-"
                self.ablesung_table.insert("", "end", values=(ablesung["datum"], ablesung["zählerstand"], verbrauch, kosten))
                prev_zählerstand = ablesung["zählerstand"]

    def clear_ablesung_entries(self):
        self.datum.set_date(datetime.now().strftime("%d.%m.%Y"))
        self.zählerstand.delete(0, tk.END)

    def show_context_menu_ablesung(self, event):
        row = self.ablesung_table.identify_row(event.y)
        if row:
            self.context_menu_ablesung.post(event.x_root, event.y_root)

    def send_to_rechnung(self):
        selected_items = self.ablesung_table.selection()
        if not selected_items:
            messagebox.showwarning("Warnung", "Bitte mindestens einen Eintrag auswählen!")
            return
        self.selected_ablesung_data = []
        for item in selected_items:
            values = self.ablesung_table.item(item, "values")
            self.selected_ablesung_data.append({"datum": values[0], "kosten": values[3]})
        self.open_rechnung_window()

    def open_rechnung_window(self):
        window = tk.Toplevel(self.root)
        window.title("Rechnung erstellen")
        window.geometry("300x150")

        ttk.Label(window, text="Rechnungsnummer:").grid(row=0, column=0, padx=5, pady=5)
        self.rechnungsnummer_entry = ttk.Entry(window)
        self.rechnungsnummer_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(window, text="Datum:").grid(row=1, column=0, padx=5, pady=5)
        self.datum_entry = DateEntry(window, date_pattern="dd.mm.yyyy")
        self.datum_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(window, text="Speichern", command=self.save_to_rechnungen).grid(row=2, column=0, columnspan=2, pady=10)

    def save_to_rechnungen(self):
        rechnungsnummer = self.rechnungsnummer_entry.get()
        datum = self.datum_entry.get()
        if not all([rechnungsnummer, datum]):
            messagebox.showerror("Fehler", "Rechnungsnummer und Datum müssen ausgefüllت sein!")
            return
        total_kosten = sum(float(item["kosten"]) if item["kosten"] != "-" else 0 for item in self.selected_ablesung_data)
        rechnung = {
            "vertragskonto": self.current_contract,
            "rechnungsnummer": rechnungsnummer,
            "datum": datum,
            "betrag": str(total_kosten),
            "pdf_path": "-"
        }
        if "rechnungen" not in self.data:
            self.data["rechnungen"] = []
        self.data["rechnungen"].append(rechnung)
        self.app.save_data()  # تغییر به self.app.save_data()
        messagebox.showinfo("Erfolg", "Rechnung wurde به Rechnungen übertragen!")
        self.app.rechnungen_manager.update_rechnungen_table()  # آپدیت جدول Rechnungen