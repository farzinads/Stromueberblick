from base import tk, ttk, messagebox, DateEntry, os
from ablesung_manager import AblesungManager
from tarif_manager import TarifManager
from rechnungen_manager import RechnungenManager
from zahlung_manager import ZahlungManager
from details_tabs import DetailsTabs

class ContractManager:
    def __init__(self, app):
        self.app = app
        self.root = app.root
        self.data = app.data
        self.contract_frame = app.contract_frame
        self.current_contract = None
        self.setup_contract_page()

    def setup_contract_page(self):
        fields = [("Anbieter:", "company"), ("Anschrift:", "company_address"), ("Telefonnummer:", "phone"),
                  ("E-Mail:", "email"), ("Vertragskontonummer:", "vertragskonto"), ("Zählernummer:", "zählernummer"),
                  ("Vertragsbeginn:", "start_date")]

        self.contract_entries = {}
        input_frame = ttk.Frame(self.contract_frame)
        input_frame.grid(row=0, column=0, sticky="nw", pady=10, padx=10)

        ttk.Label(input_frame, text="Vertragstyp:").grid(row=0, column=0, pady=5, sticky="w")
        self.contract_type = ttk.Combobox(input_frame, values=["Hausstrom", "Wärmpumpe", "Gewerbestrom", "Nachtstrom", "Ökostrom"])
        self.contract_type.grid(row=0, column=1, pady=5, sticky="ew")
        self.contract_type.set("Hausstrom")

        for i, (label_text, field) in enumerate(fields, start=1):
            ttk.Label(input_frame, text=label_text).grid(row=i, column=0, pady=5, sticky="w")
            entry = DateEntry(input_frame, date_pattern="dd.mm.yyyy") if field == "start_date" else ttk.Entry(input_frame)
            entry.grid(row=i, column=1, pady=5, sticky="ew")
            self.contract_entries[field] = entry

        ttk.Button(input_frame, text="Vertrag speichern", command=self.save_contract).grid(row=len(fields)+1, column=0, columnspan=2, pady=10)

        self.beenden_button = ttk.Button(self.contract_frame, text="Beenden", command=self.root.quit, width=10)
        self.beenden_button.place(x=975, y=5, anchor="ne")

        filter_frame = ttk.Frame(self.contract_frame)
        filter_frame.grid(row=1, column=0, pady=5, sticky="ew")

        ttk.Label(filter_frame, text="Filtern nach Anbieter:").grid(row=0, column=0, padx=5)
        self.filter_company = ttk.Entry(filter_frame)
        self.filter_company.grid(row=0, column=1, padx=5)
        self.filter_company.bind("<KeyRelease>", self.filter_contracts)

        ttk.Label(filter_frame, text="Filtern nach Vertragstyp:").grid(row=0, column=2, padx=5)
        self.filter_type = ttk.Combobox(filter_frame, values=["", "Hausstrom", "Wärmpumpe", "Gewerbestrom", "Nachtstrom", "Ökostrom"])
        self.filter_type.grid(row=0, column=3, padx=5)
        self.filter_type.bind("<<ComboboxSelected>>", self.filter_contracts)

        table_frame = ttk.Frame(self.contract_frame, relief="solid", borderwidth=2)
        table_frame.grid(row=2, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

        self.contract_table = ttk.Treeview(table_frame, columns=("Kontonummer", "Zählernummer", "Anbieter", "Vertragstyp"), show="headings")
        self.contract_table.heading("Kontonummer", text="Vertragskontonummer")
        self.contract_table.heading("Zählernummer", text="Zählernummer")
        self.contract_table.heading("Anbieter", text="Anbieter")
        self.contract_table.heading("Vertragstyp", text="Vertragstyp")
        self.contract_table.column("Kontonummer", width=150, anchor="center")
        self.contract_table.column("Zählernummer", width=150, anchor="center")
        self.contract_table.column("Anbieter", width=150, anchor="center")
        self.contract_table.column("Vertragstyp", width=150, anchor="center")
        self.contract_table.pack(fill="both", expand=True)

        self.contract_frame.grid_rowconfigure(2, weight=1)
        self.contract_frame.grid_columnconfigure(0, weight=1)

        self.context_menu_contract = tk.Menu(self.root, tearoff=0)
        self.context_menu_contract.add_command(label="Öffnen", command=self.open_contract)
        self.context_menu_contract.add_command(label="Bearbeiten", command=self.edit_contract)
        self.context_menu_contract.add_command(label="Löschen", command=self.delete_contract)
        self.contract_table.bind("<Button-3>", self.show_context_menu_contract)
        self.contract_table.bind("<Double-1>", lambda event: self.open_contract())

        self.filter_contracts(None)

    def save_contract(self):
        contract = {"contract_type": self.contract_type.get()}
        contract.update({field: self.contract_entries[field].get() for field in self.contract_entries})
        if not contract["vertragskonto"]:
            messagebox.showerror("Fehler", "Vertragskontonummer ist erforderlich!")
            return
        for existing in self.data["contracts"]:
            if existing["vertragskonto"] == contract["vertragskonto"]:
                messagebox.showerror("Fehler", "Dieser Vertrag existiert bereits!")
                return
        self.data["contracts"].append(contract)
        self.contract_table.insert("", "end", values=(contract["vertragskonto"], contract["zählernummer"], contract["company"], contract["contract_type"]))
        self.app.save_data()
        messagebox.showinfo("Erfolg", "Vertrag wurde gespeichert!")
        self.clear_contract_entries()
        self.filter_contracts(None)

    def edit_contract(self):
        selected = self.contract_table.selection()
        if not selected:
            messagebox.showwarning("Warnung", "Bitte einen Vertrag auswählen!")
            return
        values = self.contract_table.item(selected[0], "values")
        for i, contract in enumerate(self.data["contracts"]):
            if contract["vertragskonto"] == values[0]:
                self.contract_type.set(contract["contract_type"])
                for field in self.contract_entries:
                    self.contract_entries[field].delete(0, tk.END)
                    if field == "start_date":
                        self.contract_entries[field].set_date(contract[field])
                    else:
                        self.contract_entries[field].insert(0, contract[field])
                self.data["contracts"].pop(i)
                self.contract_table.delete(selected[0])
                self.app.save_data()
                messagebox.showinfo("Info", "Vertrag zum Bearbeiten geladen. Ändern و erneut speichern!")
                break
        self.filter_contracts(None)

    def delete_contract(self):
        selected = self.contract_table.selection()
        if not selected:
            messagebox.showwarning("Warnung", "Bitte einen Vertrag auswählen!")
            return
        values = self.contract_table.item(selected[0], "values")
        for i, contract in enumerate(self.data["contracts"]):
            if contract["vertragskonto"] == values[0]:
                self.data["contracts"].pop(i)
                self.contract_table.delete(selected[0])
                self.app.save_data()
                messagebox.showinfo("Erfolg", "Vertrag wurde gelöscht!")
                break
        self.filter_contracts(None)

    def filter_contracts(self, event):
        self.contract_table.delete(*self.contract_table.get_children())
        company_filter = self.filter_company.get().lower()
        type_filter = self.filter_type.get()
        for contract in self.data["contracts"]:
            if (company_filter in contract["company"].lower() and
                (not type_filter or contract["contract_type"] == type_filter)):
                self.contract_table.insert("", "end", values=(contract["vertragskonto"], contract["zählernummer"], contract["company"], contract["contract_type"]))

    def open_contract(self):
        selected = self.contract_table.selection()
        if not selected:
            messagebox.showwarning("Warnung", "Bitte einen Vertrag auswählen!")
            return
        self.current_contract = self.contract_table.item(selected[0], "values")[0]

        # پنجره جدید برای تب‌ها
        contract_window = tk.Toplevel(self.root)
        contract_window.title(f"Vertrag: {self.current_contract}")
        contract_window.geometry("1000x650")

        notebook = ttk.Notebook(contract_window)
        notebook.pack(fill="both", expand=True)

        # تب‌ها
        tarif_tab = ttk.Frame(notebook)
        ablesung_tab = ttk.Frame(notebook)
        energiekosten_tab = ttk.Frame(notebook)
        zahlungen_tab = ttk.Frame(notebook)
        rechnungen_tab = ttk.Frame(notebook)
        details_tab = ttk.Frame(notebook)

        notebook.add(tarif_tab, text="Tarifedaten")
        notebook.add(ablesung_tab, text="Ablesung")
        notebook.add(energiekosten_tab, text="Energiekosten")
        notebook.add(zahlungen_tab, text="Zahlungen")
        notebook.add(rechnungen_tab, text="Rechnungen")
        notebook.add(details_tab, text="Details")

        # راه‌اندازی مدیرها
        self.tarif_manager = TarifManager(self, tarif_tab)
        self.ablesung_manager = AblesungManager(self, ablesung_tab)
        self.energiekosten_manager = AblesungManager(self, energiekosten_tab)  # موقتاً
        self.zahlung_manager = ZahlungManager(self, zahlungen_tab)
        self.rechnungen_manager = RechnungenManager(self, rechnungen_tab)
        self.details_manager = DetailsTabs(self, details_tab)

        self.tarif_manager.setup_tarif_tab()
        self.ablesung_manager.setup_ablesung_tab()
        self.energiekosten_manager.setup_ablesung_tab()  # موقتاً
        self.zahlung_manager.setup_zahlung_tab()
        self.rechnungen_manager.setup_rechnungen_tab()
        self.details_manager.setup_details_tabs()

    def clear_contract_entries(self):
        self.contract_type.set("Hausstrom")
        for entry in self.contract_entries.values():
            if isinstance(entry, DateEntry):
                entry.set_date("01.01.2024")
            else:
                entry.delete(0, tk.END)

    def show_context_menu_contract(self, event):
        row = self.contract_table.identify_row(event.y)
        if row:
            self.contract_table.selection_set(row)
            self.context_menu_contract.post(event.x_root, event.y_root)