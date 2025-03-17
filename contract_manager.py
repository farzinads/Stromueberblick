from base import tk, ttk, messagebox, DateEntry

class ContractManager:
    def __init__(self, app):
        self.app = app
        self.root = app.root
        self.data = app.data
        self.current_contract = app.current_contract
        self.contract_frame = app.contract_frame
        self.setup_contract_frame()

    def setup_contract_frame(self):
        for widget in self.contract_frame.winfo_children():
            widget.destroy()

        # فرم ورودی
        input_frame = ttk.Frame(self.contract_frame)
        input_frame.pack(pady=10, padx=10)

        ttk.Label(input_frame, text="Vertragskontonummer:").grid(row=0, column=0, pady=5, sticky="w")
        self.contract_entry = ttk.Entry(input_frame)
        self.contract_entry.grid(row=0, column=1, pady=5, sticky="w")

        ttk.Label(input_frame, text="Anbieter:").grid(row=1, column=0, pady=5, sticky="w")
        self.anbieter = ttk.Entry(input_frame)
        self.anbieter.grid(row=1, column=1, pady=5, sticky="w")

        ttk.Label(input_frame, text="Adresse:").grid(row=2, column=0, pady=5, sticky="w")
        self.adresse = ttk.Entry(input_frame)
        self.adresse.grid(row=2, column=1, pady=5, sticky="w")

        ttk.Label(input_frame, text="Tel.nummer:").grid(row=3, column=0, pady=5, sticky="w")
        self.tel_nummer = ttk.Entry(input_frame)
        self.tel_nummer.grid(row=3, column=1, pady=5, sticky="w")

        ttk.Label(input_frame, text="E.Mailadresse:").grid(row=4, column=0, pady=5, sticky="w")
        self.email = ttk.Entry(input_frame)
        self.email.grid(row=4, column=1, pady=5, sticky="w")

        ttk.Label(input_frame, text="Vertragstyp:").grid(row=5, column=0, pady=5, sticky="w")
        self.vertragstyp = ttk.Combobox(input_frame, values=["Privat", "Gewerbe"])
        self.vertragstyp.grid(row=5, column=1, pady=5, sticky="w")
        self.vertragstyp.set("Privat")

        ttk.Label(input_frame, text="Vertragsbeginn:").grid(row=6, column=0, pady=5, sticky="w")
        self.vertragsbeginn = DateEntry(input_frame, date_pattern="dd.mm.yyyy")
        self.vertragsbeginn.grid(row=6, column=1, pady=5, sticky="w")

        ttk.Button(input_frame, text="Speichern", command=self.add_contract).grid(row=7, column=0, columnspan=2, pady=10)

        # جدول قراردادها
        table_frame = ttk.Frame(self.contract_frame)
        table_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.contract_table = ttk.Treeview(table_frame, columns=("Vertragskonto", "Anbieter", "Adresse", "Tel", "Email", "Vertragstyp", "Beginn"), show="headings")
        self.contract_table.heading("Vertragskonto", text="Vertragskontonummer")
        self.contract_table.heading("Anbieter", text="Anbieter")
        self.contract_table.heading("Adresse", text="Adresse")
        self.contract_table.heading("Tel", text="Tel.nummer")
        self.contract_table.heading("Email", text="E.Mailadresse")
        self.contract_table.heading("Vertragstyp", text="Vertragstyp")
        self.contract_table.heading("Beginn", text="Vertragsbeginn")
        self.contract_table.column("Vertragskonto", width=120, anchor="center")
        self.contract_table.column("Anbieter", width=150, anchor="center")
        self.contract_table.column("Adresse", width=200, anchor="center")
        self.contract_table.column("Tel", width=100, anchor="center")
        self.contract_table.column("Email", width=200, anchor="center")
        self.contract_table.column("Vertragstyp", width=100, anchor="center")
        self.contract_table.column("Beginn", width=100, anchor="center")
        self.contract_table.pack(fill="both", expand=True)

        self.contract_table.bind("<Double-1>", self.on_double_click)

        self.update_contract_table()

    def add_contract(self):
        vertragskonto = self.contract_entry.get().strip()
        if not vertragskonto:
            messagebox.showerror("Fehler", "Vertragskontonummer darf nicht leer sein!")
            return
        if any(c["vertragskonto"] == vertragskonto for c in self.data["contracts"]):
            messagebox.showerror("Fehler", "Dieses Vertragskonto existiert bereits!")
            return
        contract = {
            "vertragskonto": vertragskonto,
            "anbieter": self.anbieter.get().strip(),
            "adresse": self.adresse.get().strip(),
            "tel_nummer": self.tel_nummer.get().strip(),
            "email": self.email.get().strip(),
            "vertragstyp": self.vertragstyp.get(),
            "vertragsbeginn": self.vertragsbeginn.get()
        }
        if not contract["anbieter"] or not contract["vertragsbeginn"]:
            messagebox.showerror("Fehler", "Anbieter und Vertragsbeginn dürfen nicht leer sein!")
            return
        self.data["contracts"].append(contract)
        self.app.save_data()
        self.clear_entries()
        self.update_contract_table()
        messagebox.showinfo("Erfolg", f"Vertrag {vertragskonto} wurde hinzugefügt!")

    def clear_entries(self):
        self.contract_entry.delete(0, tk.END)
        self.anbieter.delete(0, tk.END)
        self.adresse.delete(0, tk.END)
        self.tel_nummer.delete(0, tk.END)
        self.email.delete(0, tk.END)
        self.vertragstyp.set("Privat")
        self.vertragsbeginn.set_date("01.01.2025")

    def update_contract_table(self):
        self.contract_table.delete(*self.contract_table.get_children())
        for contract in self.data["contracts"]:
            self.contract_table.insert("", "end", values=(
                contract["vertragskonto"],
                contract["anbieter"],
                contract["adresse"],
                contract["tel_nummer"],
                contract["email"],
                contract["vertragstyp"],
                contract["vertragsbeginn"]
            ))

    def on_double_click(self, event):
        item = self.contract_table.selection()
        if item:
            vertragskonto = self.contract_table.item(item, "values")[0]
            self.app.current_contract = vertragskonto
            self.current_contract = vertragskonto
            self.app.show_tabs()