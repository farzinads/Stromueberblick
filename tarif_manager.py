from base import tk, ttk, messagebox, DateEntry

class TarifManager:
    def __init__(self, app):
        self.app = app
        self.root = app.root
        self.data = app.data
        self.current_contract = app.current_contract
        self.tarifedaten_tab = app.tarifedaten_tab
        self.ablesung_tab = app.ablesung_tab  # اضافه کردن تب Ablesung
        self.setup_tarifedaten_tab()
        self.setup_ablesung_tab()

    def setup_tarifedaten_tab(self):
        for widget in self.tarifedaten_tab.winfo_children():
            widget.destroy()

        # فرم ورودی
        input_frame = ttk.Frame(self.tarifedaten_tab)
        input_frame.pack(pady=10, padx=10, anchor="nw")

        # Zeitraum
        ttk.Label(input_frame, text="Zeitraum:").grid(row=0, column=0, pady=5, sticky="w")
        ttk.Label(input_frame, text="Von:").grid(row=0, column=1, pady=5, sticky="w")
        self.von_date = DateEntry(input_frame, date_pattern="dd.mm.yyyy", width=12)
        self.von_date.grid(row=0, column=2, pady=5, sticky="w")
        ttk.Label(input_frame, text="Bis:").grid(row=0, column=3, pady=5, sticky="w")
        self.bis_date = DateEntry(input_frame, date_pattern="dd.mm.yyyy", width=12)
        self.bis_date.grid(row=0, column=4, pady=5, sticky="w")

        # فیلدها و کدهای شناسایی
        ttk.Label(input_frame, text="Arbeitspreis HT (kWh):").grid(row=1, column=0, pady=5, sticky="w")
        self.arbeitspreis_ht = ttk.Entry(input_frame, width=15)
        self.arbeitspreis_ht.grid(row=1, column=1, pady=5, sticky="w")
        ttk.Label(input_frame, text="ID:").grid(row=1, column=2, pady=5, sticky="w")
        self.arbeitspreis_ht_id = ttk.Entry(input_frame, width=10)
        self.arbeitspreis_ht_id.grid(row=1, column=3, pady=5, sticky="w")

        ttk.Label(input_frame, text="Arbeitspreis NT (kWh):").grid(row=2, column=0, pady=5, sticky="w")
        self.arbeitspreis_nt = ttk.Entry(input_frame, width=15)
        self.arbeitspreis_nt.grid(row=2, column=1, pady=5, sticky="w")
        ttk.Label(input_frame, text="ID:").grid(row=2, column=2, pady=5, sticky="w")
        self.arbeitspreis_nt_id = ttk.Entry(input_frame, width=10)
        self.arbeitspreis_nt_id.grid(row=2, column=3, pady=5, sticky="w")

        ttk.Label(input_frame, text="Grundpreis (€/Jahr):").grid(row=3, column=0, pady=5, sticky="w")
        self.grundpreis = ttk.Entry(input_frame, width=15)
        self.grundpreis.grid(row=3, column=1, pady=5, sticky="w")
        ttk.Label(input_frame, text="ID:").grid(row=3, column=2, pady=5, sticky="w")
        self.grundpreis_id = ttk.Entry(input_frame, width=10)
        self.grundpreis_id.grid(row=3, column=3, pady=5, sticky="w")

        ttk.Label(input_frame, text="Zähler (€/Jahr):").grid(row=4, column=0, pady=5, sticky="w")
        self.zähler = ttk.Entry(input_frame, width=15)
        self.zähler.grid(row=4, column=1, pady=5, sticky="w")
        ttk.Label(input_frame, text="ID:").grid(row=4, column=2, pady=5, sticky="w")
        self.zähler_id = ttk.Entry(input_frame, width=10)
        self.zähler_id.grid(row=4, column=3, pady=5, sticky="w")

        # دکمه Speichern
        self.save_button = ttk.Button(input_frame, text="Speichern", command=self.save_tarif)
        self.save_button.grid(row=5, column=1, pady=5, sticky="w")
        self.save_button.configure(style="Red.TButton")
        style = ttk.Style()
        style.configure("Red.TButton", foreground="red", font=("Arial", 10, "bold"))

        # جدول
        table_frame = ttk.Frame(self.tarifedaten_tab, relief="solid", borderwidth=2)
        table_frame.pack(pady=25, padx=10, fill="both", expand=True)

        self.tarif_table = ttk.Treeview(table_frame, columns=("Von", "Bis", "HT", "HT_ID", "NT", "NT_ID", "Grundpreis", "Grundpreis_ID", "Zähler", "Zähler_ID"), show="headings")
        self.tarif_table.heading("Von", text="Von")
        self.tarif_table.heading("Bis", text="Bis")
        self.tarif_table.heading("HT", text="Arbeitspreis HT")
        self.tarif_table.heading("HT_ID", text="HT ID")
        self.tarif_table.heading("NT", text="Arbeitspreis NT")
        self.tarif_table.heading("NT_ID", text="NT ID")
        self.tarif_table.heading("Grundpreis", text="Grundpreis")
        self.tarif_table.heading("Grundpreis_ID", text="Grundpreis ID")
        self.tarif_table.heading("Zähler", text="Zähler")
        self.tarif_table.heading("Zähler_ID", text="Zähler ID")
        self.tarif_table.column("Von", width=80, anchor="center")
        self.tarif_table.column("Bis", width=80, anchor="center")
        self.tarif_table.column("HT", width=100, anchor="center")
        self.tarif_table.column("HT_ID", width=80, anchor="center")
        self.tarif_table.column("NT", width=100, anchor="center")
        self.tarif_table.column("NT_ID", width=80, anchor="center")
        self.tarif_table.column("Grundpreis", width=100, anchor="center")
        self.tarif_table.column("Grundpreis_ID", width=80, anchor="center")
        self.tarif_table.column("Zähler", width=100, anchor="center")
        self.tarif_table.column("Zähler_ID", width=80, anchor="center")
        self.tarif_table.pack(fill="both", expand=True)

        style.configure("Treeview", rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        self.tarif_table.tag_configure("oddrow", background="#d3d3d3")
        self.tarif_table.tag_configure("evenrow", background="#ffffff")

        self.update_tarif_table()

    def save_tarif(self):
        tarif = {
            "vertragskonto": self.current_contract or "default",  # اگه current_contract نبود، یه مقدار پیش‌فرض
            "von": self.von_date.get(),
            "bis": self.bis_date.get(),
            "arbeitspreis_ht": self.arbeitspreis_ht.get().strip(),
            "arbeitspreis_ht_id": self.arbeitspreis_ht_id.get().strip(),
            "arbeitspreis_nt": self.arbeitspreis_nt.get().strip(),
            "arbeitspreis_nt_id": self.arbeitspreis_nt_id.get().strip(),
            "grundpreis": self.grundpreis.get().strip(),
            "grundpreis_id": self.grundpreis_id.get().strip(),
            "zähler": self.zähler.get().strip(),
            "zähler_id": self.zähler_id.get().strip()
        }
        if not all([tarif["arbeitspreis_ht"], tarif["grundpreis"], tarif["von"]]):  # Von هم اجباری
            messagebox.showerror("Fehler", "Arbeitspreis HT, Grundpreis und Von dürfen nicht leer sein!")
            return
        if "tarife" not in self.data:
            self.data["tarife"] = []
        self.data["tarife"].append(tarif)
        self.app.save_data()
        self.clear_tarif_entries()
        self.update_tarif_table()
        messagebox.showinfo("Erfolg", "Tarifdaten wurden gespeichert!")

    def clear_tarif_entries(self):
        self.von_date.set_date("01.01.2025")
        self.bis_date.set_date("31.12.2025")
        self.arbeitspreis_ht.delete(0, tk.END)
        self.arbeitspreis_ht_id.delete(0, tk.END)
        self.arbeitspreis_nt.delete(0, tk.END)
        self.arbeitspreis_nt_id.delete(0, tk.END)
        self.grundpreis.delete(0, tk.END)
        self.grundpreis_id.delete(0, tk.END)
        self.zähler.delete(0, tk.END)
        self.zähler_id.delete(0, tk.END)

    def update_tarif_table(self):
        self.tarif_table.delete(*self.tarif_table.get_children())
        if "tarife" in self.data and self.current_contract:
            for i, tarif in enumerate(self.data["tarife"]):
                if tarif["vertragskonto"] == self.current_contract:
                    tag = "evenrow" if i % 2 == 0 else "oddrow"
                    self.tarif_table.insert("", "end", values=(
                        tarif["von"],
                        tarif["bis"],
                        tarif["arbeitspreis_ht"],
                        tarif["arbeitspreis_ht_id"],
                        tarif["arbeitspreis_nt"],
                        tarif["arbeitspreis_nt_id"],
                        tarif["grundpreis"],
                        tarif["grundpreis_id"],
                        tarif["zähler"],
                        tarif["zähler_id"]
                    ), tags=(tag,))

    def setup_ablesung_tab(self):
        for widget in self.ablesung_tab.winfo_children():
            widget.destroy()

        # فرم ورودی
        input_frame = ttk.Frame(self.ablesung_tab)
        input_frame.pack(pady=10, padx=10, anchor="nw")

        ttk.Label(input_frame, text="Ablesungsdatum:").grid(row=0, column=0, pady=5, sticky="w")
        self.ablesungsdatum = DateEntry(input_frame, date_pattern="dd.mm.yyyy", width=15)
        self.ablesungsdatum.grid(row=0, column=1, pady=5, sticky="w")

        ttk.Label(input_frame, text="Zählerstand HT:").grid(row=1, column=0, pady=5, sticky="w")
        self.zählerstand_ht = ttk.Entry(input_frame, width=15)
        self.zählerstand_ht.grid(row=1, column=1, pady=5, sticky="w")

        ttk.Label(input_frame, text="Zählerstand NT:").grid(row=2, column=0, pady=5, sticky="w")
        self.zählerstand_nt = ttk.Entry(input_frame, width=15)
        self.zählerstand_nt.grid(row=2, column=1, pady=5, sticky="w")

        # دکمه Speichern
        self.ablesung_save_button = ttk.Button(input_frame, text="Speichern", command=self.save_ablesung)
        self.ablesung_save_button.grid(row=3, column=1, pady=5, sticky="w")
        self.ablesung_save_button.configure(style="Red.TButton")

        # جدول
        table_frame = ttk.Frame(self.ablesung_tab, relief="solid", borderwidth=2)
        table_frame.pack(pady=25, padx=10, fill="both", expand=True)

        self.ablesung_table = ttk.Treeview(table_frame, columns=("Datum", "HT", "NT"), show="headings")
        self.ablesung_table.heading("Datum", text="Ablesungsdatum")
        self.ablesung_table.heading("HT", text="Zählerstand HT")
        self.ablesung_table.heading("NT", text="Zählerstand NT")
        self.ablesung_table.column("Datum", width=120, anchor="center")
        self.ablesung_table.column("HT", width=120, anchor="center")
        self.ablesung_table.column("NT", width=120, anchor="center")
        self.ablesung_table.pack(fill="both", expand=True)

        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        self.ablesung_table.tag_configure("oddrow", background="#d3d3d3")
        self.ablesung_table.tag_configure("evenrow", background="#ffffff")

        self.update_ablesung_table()

    def save_ablesung(self):
        ablesung = {
            "vertragskonto": self.current_contract or "default",
            "ablesungsdatum": self.ablesungsdatum.get(),
            "zählerstand_ht": self.zählerstand_ht.get().strip(),
            "zählerstand_nt": self.zählerstand_nt.get().strip()
        }
        if not all([ablesung["ablesungsdatum"], ablesung["zählerstand_ht"]]):  # HT اجباری
            messagebox.showerror("Fehler", "Ablesungsdatum und Zählerstand HT dürfen nicht leer sein!")
            return
        if "ablesungen" not in self.data:
            self.data["ablesungen"] = []
        self.data["ablesungen"].append(ablesung)
        self.app.save_data()
        self.clear_ablesung_entries()
        self.update_ablesung_table()
        messagebox.showinfo("Erfolg", "Ablesung wurde gespeichert!")

    def clear_ablesung_entries(self):
        self.ablesungsdatum.set_date("01.01.2025")
        self.zählerstand_ht.delete(0, tk.END)
        self.zählerstand_nt.delete(0, tk.END)

    def update_ablesung_table(self):
        self.ablesung_table.delete(*self.ablesung_table.get_children())
        if "ablesungen" in self.data and self.current_contract:
            for i, ablesung in enumerate(self.data["ablesungen"]):
                if ablesung["vertragskonto"] == self.current_contract:
                    tag = "evenrow" if i % 2 == 0 else "oddrow"
                    self.ablesung_table.insert("", "end", values=(
                        ablesung["ablesungsdatum"],
                        ablesung["zählerstand_ht"],
                        ablesung["zählerstand_nt"]
                    ), tags=(tag,))