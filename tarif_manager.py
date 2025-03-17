from base import tk, ttk, messagebox, DateEntry

class TarifManager:
    def __init__(self, app):
        self.app = app
        self.root = app.root
        self.data = app.data
        self.current_contract = app.current_contract
        self.tarifedaten_tab = app.tarifedaten_tab
        self.setup_tarifedaten_tab()

    def setup_tarifedaten_tab(self):
        # فرم ورودی
        input_frame = ttk.Frame(self.tarifedaten_tab)
        input_frame.pack(pady=10, padx=10)

        # فیلدها
        ttk.Label(input_frame, text="Anbieter:").grid(row=0, column=0, pady=5, sticky="w")
        self.anbieter = ttk.Entry(input_frame)
        self.anbieter.grid(row=0, column=1, pady=5, sticky="w")

        ttk.Label(input_frame, text="Adresse:").grid(row=1, column=0, pady=5, sticky="w")
        self.adresse = ttk.Entry(input_frame)
        self.adresse.grid(row=1, column=1, pady=5, sticky="w")

        ttk.Label(input_frame, text="Tel.nummer:").grid(row=2, column=0, pady=5, sticky="w")
        self.tel_nummer = ttk.Entry(input_frame)
        self.tel_nummer.grid(row=2, column=1, pady=5, sticky="w")

        ttk.Label(input_frame, text="E.Mailadresse:").grid(row=3, column=0, pady=5, sticky="w")
        self.email = ttk.Entry(input_frame)
        self.email.grid(row=3, column=1, pady=5, sticky="w")

        ttk.Label(input_frame, text="Vertragstyp:").grid(row=4, column=0, pady=5, sticky="w")
        self.vertragstyp = ttk.Combobox(input_frame, values=["Privat", "Gewerbe"])
        self.vertragstyp.grid(row=4, column=1, pady=5, sticky="w")
        self.vertragstyp.set("Privat")  # پیش‌فرض

        ttk.Label(input_frame, text="Vertragsbeginn:").grid(row=5, column=0, pady=5, sticky="w")
        self.vertragsbeginn = DateEntry(input_frame, date_pattern="dd.mm.yyyy")
        self.vertragsbeginn.grid(row=5, column=1, pady=5, sticky="w")

        # دکمه Speichern
        ttk.Button(input_frame, text="Speichern", command=self.save_tarif).grid(row=6, column=0, columnspan=2, pady=10)

        # فیلتر
        filter_frame = ttk.Frame(self.tarifedaten_tab)
        filter_frame.pack(pady=5, padx=10, fill="x")

        ttk.Label(filter_frame, text="Filter Anbieter:").pack(side="left", padx=5)
        self.filter_anbieter = ttk.Entry(filter_frame)
        self.filter_anbieter.pack(side="left", padx=5)
        self.filter_anbieter.bind("<KeyRelease>", self.apply_filter)

        ttk.Label(filter_frame, text="Filter Vertragstyp:").pack(side="left", padx=5)
        self.filter_vertragstyp = ttk.Combobox(filter_frame, values=["", "Privat", "Gewerbe"])
        self.filter_vertragstyp.pack(side="left", padx=5)
        self.filter_vertragstyp.bind("<<ComboboxSelected>>", self.apply_filter)

        # جدول
        table_frame = ttk.Frame(self.tarifedaten_tab, relief="solid", borderwidth=2)
        table_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.tarif_table = ttk.Treeview(table_frame, columns=("Anbieter", "Adresse", "Tel", "Email", "Vertragstyp", "Beginn"), show="headings")
        self.tarif_table.heading("Anbieter", text="Anbieter")
        self.tarif_table.heading("Adresse", text="Adresse")
        self.tarif_table.heading("Tel", text="Tel.nummer")
        self.tarif_table.heading("Email", text="E.Mailadresse")
        self.tarif_table.heading("Vertragstyp", text="Vertragstyp")
        self.tarif_table.heading("Beginn", text="Vertragsbeginn")
        self.tarif_table.column("Anbieter", width=150, anchor="center")
        self.tarif_table.column("Adresse", width=200, anchor="center")
        self.tarif_table.column("Tel", width=100, anchor="center")
        self.tarif_table.column("Email", width=200, anchor="center")
        self.tarif_table.column("Vertragstyp", width=100, anchor="center")
        self.tarif_table.column("Beginn", width=100, anchor="center")
        self.tarif_table.pack(fill="both", expand=True)

        self.update_tarif_table()

    def save_tarif(self):
        if not self.current_contract:
            messagebox.showerror("Fehler", "Kein Vertrag ausgewählt!")
            return
        tarif = {
            "vertragskonto": self.current_contract,
            "anbieter": self.anbieter.get().strip(),
            "adresse": self.adresse.get().strip(),
            "tel_nummer": self.tel_nummer.get().strip(),
            "email": self.email.get().strip(),
            "vertragstyp": self.vertragstyp.get(),
            "vertragsbeginn": self.vertragsbeginn.get()
        }
        if not all([tarif["anbieter"], tarif["vertragsbeginn"]]):  # حداقل Anbieter و Vertragsbeginn اجباری
            messagebox.showerror("Fehler", "Anbieter und Vertragsbeginn dürfen nicht leer sein!")
            return
        self.data["tarife"].append(tarif)
        self.app.save_data()
        self.clear_entries()
        self.update_tarif_table()
        messagebox.showinfo("Erfolg", "Tarifdaten wurden gespeichert!")

    def clear_entries(self):
        self.anbieter.delete(0, tk.END)
        self.adresse.delete(0, tk.END)
        self.tel_nummer.delete(0, tk.END)
        self.email.delete(0, tk.END)
        self.vertragstyp.set("Privat")
        self.vertragsbeginn.set_date("01.01.2025")

    def update_tarif_table(self):
        self.tarif_table.delete(*self.tarif_table.get_children())
        if self.current_contract and "tarife" in self.data:
            for tarif in self.data["tarife"]:
                if tarif["vertragskonto"] == self.current_contract:
                    self.tarif_table.insert("", "end", values=(
                        tarif["anbieter"],
                        tarif["adresse"],
                        tarif["tel_nummer"],
                        tarif["email"],
                        tarif["vertragstyp"],
                        tarif["vertragsbeginn"]
                    ))

    def apply_filter(self, event=None):
        self.tarif_table.delete(*self.tarif_table.get_children())
        if not self.current_contract or "tarife" not in self.data:
            return
        filter_anbieter = self.filter_anbieter.get().strip().lower()
        filter_vertragstyp = self.filter_vertragstyp.get()
        for tarif in self.data["tarife"]:
            if tarif["vertragskonto"] == self.current_contract:
                anbieter_match = filter_anbieter in tarif["anbieter"].lower() if filter_anbieter else True
                vertragstyp_match = tarif["vertragstyp"] == filter_vertragstyp if filter_vertragstyp else True
                if anbieter_match and vertragstyp_match:
                    self.tarif_table.insert("", "end", values=(
                        tarif["anbieter"],
                        tarif["adresse"],
                        tarif["tel_nummer"],
                        tarif["email"],
                        tarif["vertragstyp"],
                        tarif["vertragsbeginn"]
                    ))