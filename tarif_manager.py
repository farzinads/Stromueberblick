import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from base import load_data, save_data

class TarifManager:
    def __init__(self, app):
        self.app = app
        self.root = app.root
        self.data = app.data
        self.tarifedaten_tab = app.tarifedaten_tab
        self.setup_tarifedaten_tab()

    def setup_tarifedaten_tab(self):
        for widget in self.tarifedaten_tab.winfo_children():
            widget.destroy()

        input_frame = ttk.Frame(self.tarifedaten_tab)
        input_frame.pack(pady=10, padx=10, anchor="nw")

        ttk.Label(input_frame, text="Zeitraum:").grid(row=0, column=0, pady=5, sticky="w")
        ttk.Label(input_frame, text="Von:").grid(row=0, column=1, pady=5, sticky="w")
        self.von_date = DateEntry(input_frame, date_pattern="dd.mm.yyyy", width=12)
        self.von_date.grid(row=0, column=2, pady=5, sticky="w")
        ttk.Label(input_frame, text="Bis:").grid(row=0, column=3, pady=5, sticky="w")
        self.bis_date = DateEntry(input_frame, date_pattern="dd.mm.yyyy", width=12)
        self.bis_date.grid(row=0, column=4, pady=5, sticky="w")

        ttk.Label(input_frame, text="Arbeitspreis HT (ct/kWh):").grid(row=1, column=0, pady=5, sticky="w")
        self.arbeitspreis_ht = ttk.Entry(input_frame, width=15)
        self.arbeitspreis_ht.grid(row=1, column=1, pady=5, padx=(0, 10), sticky="w")
        ttk.Label(input_frame, text="IDHT:").grid(row=1, column=2, pady=5, padx=(50, 0), sticky="w")
        self.idht = ttk.Entry(input_frame, width=10)
        self.idht.grid(row=1, column=3, pady=5, sticky="w")

        ttk.Label(input_frame, text="Arbeitspreis NT (ct/kWh):").grid(row=2, column=0, pady=5, sticky="w")
        self.arbeitspreis_nt = ttk.Entry(input_frame, width=15)
        self.arbeitspreis_nt.grid(row=2, column=1, pady=5, padx=(0, 10), sticky="w")
        ttk.Label(input_frame, text="IDNT:").grid(row=2, column=2, pady=5, padx=(50, 0), sticky="w")
        self.idnt = ttk.Entry(input_frame, width=10)
        self.idnt.grid(row=2, column=3, pady=5, sticky="w")

        ttk.Label(input_frame, text="Grundpreis (€/Jahr):").grid(row=3, column=0, pady=5, sticky="w")
        self.grundpreis = ttk.Entry(input_frame, width=15)
        self.grundpreis.grid(row=3, column=1, pady=5, padx=(0, 10), sticky="w")
        ttk.Label(input_frame, text="IDGR:").grid(row=3, column=2, pady=5, padx=(50, 0), sticky="w")
        self.idgr = ttk.Entry(input_frame, width=10)
        self.idgr.grid(row=3, column=3, pady=5, sticky="w")

        ttk.Label(input_frame, text="Zähler (€/Jahr):").grid(row=4, column=0, pady=5, sticky="w")
        self.zähler = ttk.Entry(input_frame, width=15)
        self.zähler.grid(row=4, column=1, pady=5, padx=(0, 10), sticky="w")
        ttk.Label(input_frame, text="IDZL:").grid(row=4, column=2, pady=5, padx=(50, 0), sticky="w")
        self.idzl = ttk.Entry(input_frame, width=10)
        self.idzl.grid(row=4, column=3, pady=5, sticky="w")

        self.save_button = ttk.Button(input_frame, text="Speichern", command=self.save_tarif)
        self.save_button.grid(row=5, column=1, pady=5, sticky="w")
        self.save_button.configure(style="Red.TButton")
        style = ttk.Style()
        style.configure("Red.TButton", foreground="red", font=("Arial", 10, "bold"))

        table_frame = ttk.Frame(self.tarifedaten_tab, relief="solid", borderwidth=2)
        table_frame.pack(pady=25, padx=10, fill="both", expand=True)

        self.tarif_table = ttk.Treeview(table_frame, columns=("Zeitraum", "HT", "NT", "Grundpreis", "Zähler"), show="headings")
        self.tarif_table.heading("Zeitraum", text="Zeitraum")
        self.tarif_table.heading("HT", text="Arbeitspreis HT")
        self.tarif_table.heading("NT", text="Arbeitspreis NT")
        self.tarif_table.heading("Grundpreis", text="Grundpreis")
        self.tarif_table.heading("Zähler", text="Zähler")
        self.tarif_table.column("Zeitraum", width=150, anchor="center")
        self.tarif_table.column("HT", width=120, anchor="center")
        self.tarif_table.column("NT", width=120, anchor="center")
        self.tarif_table.column("Grundpreis", width=120, anchor="center")
        self.tarif_table.column("Zähler", width=120, anchor="center")
        self.tarif_table.pack(fill="both", expand=True)

        style.configure("Treeview", rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        self.tarif_table.tag_configure("oddrow", background="#d3d3d3")
        self.tarif_table.tag_configure("evenrow", background="#ffffff")

        self.tarif_table.bind("<Button-3>", self.show_context_menu)
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Bearbeiten", command=self.edit_tarif)
        self.context_menu.add_command(label="Löschen", command=self.delete_tarif)

        self.update_tarif_table()

    def save_tarif(self):
        if not self.app.current_contract:
            messagebox.showerror("Fehler", "Kein Vertrag ausgewählt!")
            return
        tarif = {
            "vertragskonto": self.app.current_contract,
            "von": self.von_date.get(),
            "bis": self.bis_date.get(),
            "arbeitspreis_ht": self.arbeitspreis_ht.get().strip(),
            "idht": self.idht.get().strip() or "",
            "arbeitspreis_nt": self.arbeitspreis_nt.get().strip(),
            "idnt": self.idnt.get().strip() or "",
            "grundpreis": self.grundpreis.get().strip(),
            "idgr": self.idgr.get().strip() or "",
            "zähler": self.zähler.get().strip(),
            "idzl": self.idzl.get().strip() or ""
        }
        if not all([tarif["arbeitspreis_ht"], tarif["grundpreis"], tarif["von"]]):
            messagebox.showerror("Fehler", "Arbeitspreis HT, Grundpreis und Von dürfen nicht leer sein!")
            return
        if "tarife" not in self.data:
            self.data["tarife"] = []
        self.data["tarife"].append(tarif)
        self.app.save_data()
        self.clear_tarif_entries()
        self.update_tarif_table()
        messagebox.showinfo("Erfolg", "Tarifdaten wurden gespeichert!")
        print(f"Saved tarif: {tarif}")  # دیباگ

    def clear_tarif_entries(self):
        self.von_date.set_date("01.01.2025")
        self.bis_date.set_date("31.12.2025")
        self.arbeitspreis_ht.delete(0, tk.END)
        self.idht.delete(0, tk.END)
        self.arbeitspreis_nt.delete(0, tk.END)
        self.idnt.delete(0, tk.END)
        self.grundpreis.delete(0, tk.END)
        self.idgr.delete(0, tk.END)
        self.zähler.delete(0, tk.END)
        self.idzl.delete(0, tk.END)

    def update_tarif_table(self):
        self.tarif_table.delete(*self.tarif_table.get_children())
        if "tarife" not in self.data or not self.app.current_contract:
            print("No data or current_contract not set:", self.app.current_contract)
            return
        print(f"Updating table for contract: {self.app.current_contract}")  # دیباگ
        for i, tarif in enumerate(self.data["tarife"]):
            if tarif["vertragskonto"] == self.app.current_contract:
                zeitraum = f"{tarif['von']} - {tarif['bis']}"
                ht_display = f"{tarif['arbeitspreis_ht']} ({tarif.get('idht', '')})" if tarif.get("idht") else tarif["arbeitspreis_ht"]
                nt_display = f"{tarif['arbeitspreis_nt']} ({tarif.get('idnt', '')})" if tarif.get("idnt") else tarif["arbeitspreis_nt"]
                grundpreis_display = f"{tarif['grundpreis']} ({tarif.get('idgr', '')})" if tarif.get("idgr") else tarif["grundpreis"]
                zähler_display = f"{tarif['zähler']} ({tarif.get('idzl', '')})" if tarif.get("idzl") else tarif["zähler"]
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                self.tarif_table.insert("", "end", values=(
                    zeitraum,
                    ht_display,
                    nt_display,
                    grundpreis_display,
                    zähler_display
                ), tags=(tag,))
                print(f"Added to table: {zeitraum}")  # دیباگ

    def show_context_menu(self, event):
        item = self.tarif_table.identify_row(event.y)
        if item:
            self.tarif_table.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def edit_tarif(self):
        item = self.tarif_table.selection()
        if not item:
            return
        values = self.tarif_table.item(item, "values")
        zeitraum = values[0].split(" - ")
        for tarif in self.data["tarife"]:
            if tarif["vertragskonto"] == self.app.current_contract and f"{tarif['von']} - {tarif['bis']}" == values[0]:
                self.von_date.set_date(tarif["von"])
                self.bis_date.set_date(tarif["bis"])
                self.arbeitspreis_ht.delete(0, tk.END)
                self.arbeitspreis_ht.insert(0, tarif["arbeitspreis_ht"])
                self.idht.delete(0, tk.END)
                self.idht.insert(0, tarif.get("idht", ""))
                self.arbeitspreis_nt.delete(0, tk.END)
                self.arbeitspreis_nt.insert(0, tarif["arbeitspreis_nt"])
                self.idnt.delete(0, tk.END)
                self.idnt.insert(0, tarif.get("idnt", ""))
                self.grundpreis.delete(0, tk.END)
                self.grundpreis.insert(0, tarif["grundpreis"])
                self.idgr.delete(0, tk.END)
                self.idgr.insert(0, tarif.get("idgr", ""))
                self.zähler.delete(0, tk.END)
                self.zähler.insert(0, tarif["zähler"])
                self.idzl.delete(0, tk.END)
                self.idzl.insert(0, tarif.get("idzl", ""))
                self.data["tarife"].remove(tarif)
                self.update_tarif_table()
                self.save_button.configure(text="Aktualisieren", command=self.update_tarif)
                break

    def update_tarif(self):
        self.save_tarif()
        self.save_button.configure(text="Speichern", command=self.save_tarif)

    def delete_tarif(self):
        item = self.tarif_table.selection()
        if not item:
            return
        values = self.tarif_table.item(item, "values")
        if messagebox.askyesno("Bestätigung", f"Möchten Sie den Eintrag {values[0]} löschen?"):
            for i, tarif in enumerate(self.data["tarife"]):
                if tarif["vertragskonto"] == self.app.current_contract and f"{tarif['von']} - {tarif['bis']}" == values[0]:
                    del self.data["tarife"][i]
                    self.app.save_data()
                    self.update_tarif_table()
                    messagebox.showinfo("Erfolg", f"Eintrag {values[0]} wurde gelöscht!")
                    break