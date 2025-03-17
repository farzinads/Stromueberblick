from base import tk, ttk, messagebox, DateEntry

class ContractManager:
    def __init__(self, app):
        self.app = app
        self.root = app.root
        self.data = app.data
        self.current_contract = app.current_contract
        self.contract_frame = app.main_frame  # فعلاً از main_frame استفاده می‌کنیم
        self.setup_contract_frame()

    def setup_contract_frame(self):
        # پاک کردن محتوای قبلی main_frame
        for widget in self.contract_frame.winfo_children():
            widget.destroy()

        # فرم ورودی
        input_frame = ttk.Frame(self.contract_frame)
        input_frame.pack(pady=10, padx=10)

        ttk.Label(input_frame, text="Vertragskontonummer:").grid(row=0, column=0, pady=5, sticky="w")
        self.contract_entry = ttk.Entry(input_frame)
        self.contract_entry.grid(row=0, column=1, pady=5)

        ttk.Button(input_frame, text="Hinzufügen", command=self.add_contract).grid(row=1, column=0, columnspan=2, pady=10)

        # جدول قراردادها
        table_frame = ttk.Frame(self.contract_frame)
        table_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.contract_table = ttk.Treeview(table_frame, columns=("Vertragskonto",), show="headings")
        self.contract_table.heading("Vertragskonto", text="Vertragskontonummer")
        self.contract_table.column("Vertragskonto", width=200, anchor="center")
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
        self.data["contracts"].append({"vertragskonto": vertragskonto})
        self.app.save_data()
        self.update_contract_table()
        self.contract_entry.delete(0, tk.END)
        messagebox.showinfo("Erfolg", f"Vertrag {vertragskonto} wurde hinzugefügt!")

    def update_contract_table(self):
        self.contract_table.delete(*self.contract_table.get_children())
        for contract in self.data["contracts"]:
            self.contract_table.insert("", "end", values=(contract["vertragskonto"],))

    def on_double_click(self, event):
        item = self.contract_table.selection()
        if item:
            vertragskonto = self.contract_table.item(item, "values")[0]
            self.app.current_contract = vertragskonto
            self.current_contract = vertragskonto
            self.app.show_tabs()  # سوئیچ به تب‌ها