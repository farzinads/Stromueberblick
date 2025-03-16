from base import tk, ttk, messagebox, DateEntry, save_data, os

class ContractManager:
    def __init__(self, app):
        self.root = app.root
        self.app = app
        self.data = app.data
        self.contract_tab = app.contract_tab
        self.setup_contract_tab()

    def setup_contract_tab(self):
        contract_frame = ttk.Frame(self.contract_tab)
        contract_frame.place(x=10, y=10)

        ttk.Label(contract_frame, text="Vertragskonto:").grid(row=0, column=0, pady=5, sticky="w")
        self.vertragskonto = ttk.Entry(contract_frame)
        self.vertragskonto.grid(row=0, column=1, pady=5)

        ttk.Label(contract_frame, text="Anbieter:").grid(row=1, column=0, pady=5, sticky="w")
        self.anbieter = ttk.Entry(contract_frame)
        self.anbieter.grid(row=1, column=1, pady=5)

        ttk.Label(contract_frame, text="Startdatum:").grid(row=2, column=0, pady=5, sticky="w")
        self.startdatum = DateEntry(contract_frame, date_pattern="dd.mm.yyyy")
        self.startdatum.grid(row=2, column=1, pady=5)

        ttk.Button(contract_frame, text="Speichern", command=self.save_contract).grid(row=3, column=0, columnspan=2, pady=10)

        table_frame_contract = ttk.Frame(self.contract_tab, relief="solid", borderwidth=2)
        table_frame_contract.place(x=10, y=110, width=960, height=540)

        self.contract_table = ttk.Treeview(table_frame_contract, columns=("Vertragskonto", "Anbieter", "Startdatum"), show="headings")
        self.contract_table.heading("Vertragskonto", text="Vertragskonto")
        self.contract_table.heading("Anbieter", text="Anbieter")
        self.contract_table.heading("Startdatum", text="Startdatum")
        self.contract_table.column("Vertragskonto", width=200, anchor="center")
        self.contract_table.column("Anbieter", width=150, anchor="center")
        self.contract_table.column("Startdatum", width=150, anchor="center")

        scrollbar_contract = ttk.Scrollbar(table_frame_contract, orient="vertical", command=self.contract_table.yview)
        self.contract_table.configure(yscrollcommand=scrollbar_contract.set)
        scrollbar_contract.pack(side="right", fill="y")
        self.contract_table.pack(fill="both", expand=True)

        self.contract_table.bind("<Double-1>", lambda event: self.open_contract())

        self.context_menu_contract = tk.Menu(self.root, tearoff=0)
        self.context_menu_contract.add_command(label="Löschen", command=self.delete_contract)
        self.contract_table.bind("<Button-3>", self.show_context_menu_contract)

        self.update_contract_table()

    def save_contract(self):
        vertragskonto = self.vertragskonto.get()
        anbieter = self.anbieter.get()
        startdatum = self.startdatum.get()
        if not all([vertragskonto, anbieter, startdatum]):
            messagebox.showerror("Fehler", "Vertragskonto, Anbieter und Startdatum müssen ausgefüllت sein!")
            return
        contract = {"vertragskonto": vertragskonto, "anbieter": anbieter, "startdatum": startdatum}
        if "verträge" not in self.data:
            self.data["verträge"] = []
        if any(c["vertragskonto"] == vertragskonto for c in self.data["verträge"]):
            messagebox.showerror("Fehler", "Vertragskonto existiert bereits!")
            return
        self.data["verträge"].append(contract)
        save_data(self.data)
        messagebox.showinfo("Erfolg", "Vertrag wurde gespeichert!")
        self.clear_contract_entries()
        self.update_contract_table()

    def update_contract_table(self):
        self.contract_table.delete(*self.contract_table.get_children())
        if "verträge" in self.data:
            for contract in self.data["verträge"]:
                self.contract_table.insert("", "end", values=(contract["vertragskonto"], contract["anbieter"], contract["startdatum"]))

    def clear_contract_entries(self):
        self.vertragskonto.delete(0, tk.END)
        self.anbieter.delete(0, tk.END)
        self.startdatum.delete(0, tk.END)

    def delete_contract(self):
        selected = self.contract_table.selection()
        if not selected:
            messagebox.showwarning("Warnung", "Bitte einen Vertrag auswählen!")
            return
        vertragskonto = self.contract_table.item(selected[0], "values")[0]
        for i, contract in enumerate(self.data["verträge"]):
            if contract["vertragskonto"] == vertragskonto:
                self.data["verträge"].pop(i)
                break
        save_data(self.data)
        messagebox.showinfo("Erfolg", "Vertrag wurde gelöscht!")
        self.update_contract_table()

    def open_contract(self):
        selected = self.contract_table.selection()
        if not selected:
            messagebox.showwarning("Warnung", "Bitte einen Vertrag auswählen!")
            return
        selected_contract = self.contract_table.item(selected[0], "values")[0]
        self.app.current_contract = selected_contract
        self.app.update_all_tabs()
        # خط زیر حذف شده چون تابع وجود نداره:
        # self.app.update_verbrauchsmengen_table()