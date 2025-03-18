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

        self.contract_frame.configure(style="LightGray.TFrame")
        style = ttk.Style()
        style.configure("LightGray.TFrame", background="#B0B0B0")

        # فرم ورودی با حاشیه
        input_frame = ttk.Frame(self.contract_frame, relief="solid", borderwidth=2)
        input_frame.pack(side="left", padx=20, pady=10, anchor="nw")

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

        ttk.Label(input_frame, text="Vertragskontonummer:").grid(row=4, column=0, pady=5, sticky="w")
        self.contract_entry = ttk.Entry(input_frame)
        self.contract_entry.grid(row=4, column=1, pady=5, sticky="w")

        ttk.Label(input_frame, text="Zählernummer:").grid(row=5, column=0, pady=5, sticky="w")
        self.zählernummer = ttk.Entry(input_frame)
        self.zählernummer.grid(row=5, column=1, pady=5, sticky="w")

        ttk.Label(input_frame, text="Vertragstyp:").grid(row=6, column=0, pady=5, sticky="w")
        self.vertragstyp = ttk.Combobox(input_frame, values=["Hausstrom", "Wärmpumpe", "Wasser", "Heizung"])
        self.vertragstyp.grid(row=6, column=1, pady=5, sticky="w")
        self.vertragstyp.set("Hausstrom")

        ttk.Label(input_frame, text="Vertragsbeginn:").grid(row=7, column=0, pady=5, sticky="w")
        self.vertragsbeginn = DateEntry(input_frame, date_pattern="dd.mm.yyyy")
        self.vertragsbeginn.grid(row=7, column=1, pady=5, sticky="w")

        self.save_button = ttk.Button(input_frame, text="Speichern", command=self.add_contract)
        self.save_button.grid(row=8, column=1, pady=5, sticky="w")
        self.save_button.configure(style="Red.TButton")

        style.configure("Red.TButton", foreground="red", font=("Arial", 10, "bold"))

        # فیلترها با حاشیه
        filter_frame = ttk.Frame(self.contract_frame, relief="solid", borderwidth=2)
        filter_frame.pack(pady=5, padx=10, fill="x")

        ttk.Label(filter_frame, text="Filter Anbieter:").pack(side="left", padx=5)
        self.filter_anbieter = ttk.Entry(filter_frame)
        self.filter_anbieter.pack(side="left", padx=5)
        self.filter_anbieter.bind("<KeyRelease>", self.apply_filter)

        ttk.Label(filter_frame, text="Filter Vertragstyp:").pack(side="left", padx=5)
        self.filter_vertragstyp = ttk.Combobox(filter_frame, values=["", "Hausstrom", "Wärmpumpe", "Wasser", "Heizung"])
        self.filter_vertragstyp.pack(side="left", padx=5)
        self.filter_vertragstyp.bind("<<ComboboxSelected>>", self.apply_filter)

        # جدول قراردادها با حاشیه
        table_frame = ttk.Frame(self.contract_frame, relief="solid", borderwidth=2)
        table_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.contract_table = ttk.Treeview(table_frame, columns=("Anbieter", "Vertragskonto", "Vertragstyp", "Tel", "Email"), show="headings")
        self.contract_table.heading("Anbieter", text="Anbieter")
        self.contract_table.heading("Vertragskonto", text="Vertragskontonummer")
        self.contract_table.heading("Vertragstyp", text="Vertragstyp")
        self.contract_table.heading("Tel", text="Tel.nummer")
        self.contract_table.heading("Email", text="E.Mailadresse")
        self.contract_table.column("Anbieter", width=150, anchor="center")
        self.contract_table.column("Vertragskonto", width=120, anchor="center")
        self.contract_table.column("Vertragstyp", width=100, anchor="center")
        self.contract_table.column("Tel", width=100, anchor="center")
        self.contract_table.column("Email", width=200, anchor="center")
        self.contract_table.pack(fill="both", expand=True)

        style.configure("Treeview", rowheight=25, background="#B0B0B0")
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        self.contract_table.tag_configure("oddrow", background="#d3d3d3")
        self.contract_table.tag_configure("evenrow", background="#ffffff")

        self.contract_table.bind("<Double-1>", self.on_double_click)
        self.contract_table.bind("<Button-3>", self.show_context_menu)

        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Bearbeiten", command=self.edit_contract)
        self.context_menu.add_command(label="Löschen", command=self.delete_contract)

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
            "zählernummer": self.zählernummer.get().strip(),
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
        self.zählernummer.delete(0, tk.END)
        self.anbieter.delete(0, tk.END)
        self.adresse.delete(0, tk.END)
        self.tel_nummer.delete(0, tk.END)
        self.email.delete(0, tk.END)
        self.vertragstyp.set("Hausstrom")
        self.vertragsbeginn.set_date("01.01.2025")

    def update_contract_table(self):
        self.contract_table.delete(*self.contract_table.get_children())
        filter_anbieter = self.filter_anbieter.get().strip().lower()
        filter_vertragstyp = self.filter_vertragstyp.get()
        for i, contract in enumerate(self.data["contracts"]):
            anbieter_match = filter_anbieter in contract.get("anbieter", "").lower() if filter_anbieter else True
            vertragstyp_match = contract.get("vertragstyp", "") == filter_vertragstyp if filter_vertragstyp else True
            if anbieter_match and vertragstyp_match:
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                self.contract_table.insert("", "end", values=(
                    contract.get("anbieter", ""),
                    contract["vertragskonto"],
                    contract.get("vertragstyp", ""),
                    contract.get("tel_nummer", ""),
                    contract.get("email", "")
                ), tags=(tag,))

    def apply_filter(self, event=None):
        self.update_contract_table()

    def on_double_click(self, event):
        item = self.contract_table.selection()
        if item:
            vertragskonto = self.contract_table.item(item, "values")[1]
            self.app.current_contract = vertragskonto
            self.current_contract = vertragskonto
            self.app.show_tabs()

    def show_context_menu(self, event):
        item = self.contract_table.identify_row(event.y)
        if item:
            self.contract_table.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def edit_contract(self):
        item = self.contract_table.selection()
        if not item:
            return
        vertragskonto = self.contract_table.item(item, "values")[1]
        for contract in self.data["contracts"]:
            if contract["vertragskonto"] == vertragskonto:
                self.contract_entry.delete(0, tk.END)
                self.contract_entry.insert(0, contract["vertragskonto"])
                self.zählernummer.delete(0, tk.END)
                self.zählernummer.insert(0, contract.get("zählernummer", ""))
                self.anbieter.delete(0, tk.END)
                self.anbieter.insert(0, contract.get("anbieter", ""))
                self.adresse.delete(0, tk.END)
                self.adresse.insert(0, contract.get("adresse", ""))
                self.tel_nummer.delete(0, tk.END)
                self.tel_nummer.insert(0, contract.get("tel_nummer", ""))
                self.email.delete(0, tk.END)
                self.email.insert(0, contract.get("email", ""))
                self.vertragstyp.set(contract.get("vertragstyp", "Hausstrom"))
                self.vertragsbeginn.set_date(contract.get("vertragsbeginn", "01.01.2025"))
                self.data["contracts"].remove(contract)
                self.update_contract_table()
                self.save_button.configure(text="Aktualisieren", command=self.update_contract)
                break

    def update_contract(self):
        self.add_contract()
        self.save_button.configure(text="Speichern", command=self.add_contract)

    def delete_contract(self):
        item = self.contract_table.selection()
        if not item:
            return
        vertragskonto = self.contract_table.item(item, "values")[1]
        if messagebox.askyesno("Bestätigung", f"Möchten Sie den Vertrag {vertragskonto} löschen?"):
            for i, contract in enumerate(self.data["contracts"]):
                if contract["vertragskonto"] == vertragskonto:
                    del self.data["contracts"][i]
                    self.app.save_data()
                    self.update_contract_table()
                    messagebox.showinfo("Erfolg", f"Vertrag {vertragskonto} wurde gelöscht!")
                    break