import tkinter as tk
from tkinter import ttk, messagebox
from base import load_data, save_data

class TarifManager:
    def __init__(self, app):
        self.app = app
        self.root = app.root
        self.data = app.data
        self.tarifdaten_tab = app.tarifdaten_tab
        self.setup_tarif_tab()

    def setup_tarif_tab(self):
        for widget in self.tarifdaten_tab.winfo_children():
            widget.destroy()

        input_frame = ttk.LabelFrame(self.tarifdaten_tab, text="Tarifdaten hinzufügen", relief="solid", borderwidth=2)
        input_frame.pack(pady=10, padx=20, fill="x")

        ttk.Label(input_frame, text="Tarifbeginn (dd.mm.yyyy):").grid(row=0, column=0, padx=5, pady=5)
        self.tarifbeginn_entry = ttk.Entry(input_frame)
        self.tarifbeginn_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Tarifende (dd.mm.yyyy):").grid(row=1, column=0, padx=5, pady=5)
        self.tarifende_entry = ttk.Entry(input_frame)
        self.tarifende_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Arbeitspreis (€/kWh):").grid(row=2, column=0, padx=5, pady=5)
        self.arbeitspreis_entry = ttk.Entry(input_frame)
        self.arbeitspreis_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Grundpreis (€/Monat):").grid(row=3, column=0, padx=5, pady=5)
        self.grundpreis_entry = ttk.Entry(input_frame)
        self.grundpreis_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Zählerpreis (€/Monat):").grid(row=4, column=0, padx=5, pady=5)
        self.zählerpreis_entry = ttk.Entry(input_frame)
        self.zählerpreis_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="MwSt (%):").grid(row=5, column=0, padx=5, pady=5)
        self.mwst_entry = ttk.Entry(input_frame)
        self.mwst_entry.grid(row=5, column=1, padx=5, pady=5)

        ttk.Button(input_frame, text="Hinzufügen", command=self.add_tarif).grid(row=6, column=0, columnspan=2, pady=10)

        table_frame = ttk.Frame(self.tarifdaten_tab, relief="solid", borderwidth=2)
        table_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.tarif_table = ttk.Treeview(table_frame, columns=("Tarifbeginn", "Tarifende", "Arbeitspreis", "Grundpreis", "Zählerpreis", "MwSt"), show="headings")
        self.tarif_table.heading("Tarifbeginn", text="Tarifbeginn")
        self.tarif_table.heading("Tarifende", text="Tarifende")
        self.tarif_table.heading("Arbeitspreis", text="Arbeitspreis (€/kWh)")
        self.tarif_table.heading("Grundpreis", text="Grundpreis (€/Monat)")
        self.tarif_table.heading("Zählerpreis", text="Zählerpreis (€/Monat)")
        self.tarif_table.heading("MwSt", text="MwSt (%)")
        self.tarif_table.column("Tarifbeginn", width=100, minwidth=100, stretch=False)
        self.tarif_table.column("Tarifende", width=100, minwidth=100, stretch=False)
        self.tarif_table.column("Arbeitspreis", width=120, minwidth=120, stretch=False)
        self.tarif_table.column("Grundpreis", width=120, minwidth=120, stretch=False)
        self.tarif_table.column("Zählerpreis", width=120, minwidth=120, stretch=False)
        self.tarif_table.column("MwSt", width=80, minwidth=80, stretch=False)
        self.tarif_table.pack(fill="both", expand=True)

        style = ttk.Style()
        style.configure("Treeview", rowheight=25, font=("Arial", 10))  # فونت 10
        style.configure("Treeview.Heading", font="Arial 10 bold")
        self.tarif_table.tag_configure("oddrow", background="#d3d3d3")
        self.tarif_table.tag_configure("evenrow", background="#ffffff")

        self.tarif_table.bind("<Double-1>", self.edit_tarif)
        self.update_tarif_table()

    def add_tarif(self):
        tarifbeginn = self.tarifbeginn_entry.get()
        tarifende = self.tarifende_entry.get()
        arbeitspreis = self.arbeitspreis_entry.get()
        grundpreis = self.grundpreis_entry.get()
        zählerpreis = self.zählerpreis_entry.get()
        mwst = self.mwst_entry.get()

        if not all([tarifbeginn, tarifende, arbeitspreis]):
            messagebox.showerror("Fehler", "Tarifbeginn, Tarifende und Arbeitspreis sind Pflichtfelder!")
            return

        if "tarifdaten" not in self.data:
            self.data["tarifdaten"] = []

        self.data["tarifdaten"].append({
            "vertragskonto": self.app.current_contract,
            "tarifbeginn": tarifbeginn,
            "tarifende": tarifende,
            "arbeitspreis": arbeitspreis,
            "grundpreis": grundpreis,
            "zählerpreis": zählerpreis,
            "mwst": mwst
        })
        self.app.save_data()
        self.update_tarif_table()
        self.app.refresh_all_tabs()  # آپدیت خودکار

    def update_tarif_table(self):
        self.tarif_table.delete(*self.tarif_table.get_children())
        if "tarifdaten" not in self.data or not self.app.current_contract:
            return
        tarifdaten = [t for t in self.data["tarifdaten"] if t["vertragskonto"] == self.app.current_contract]
        for i, tarif in enumerate(tarifdaten):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tarif_table.insert("", "end", values=(
                tarif["tarifbeginn"],
                tarif["tarifende"],
                tarif["arbeitspreis"],
                tarif["grundpreis"],
                tarif["zählerpreis"],
                tarif["mwst"]
            ), tags=(tag,))

    def edit_tarif(self, event):
        item = self.tarif_table.selection()
        if not item:
            return
        index = self.tarif_table.index(item[0])
        tarifdaten = [t for t in self.data["tarifdaten"] if t["vertragskonto"] == self.app.current_contract][index]

        self.tarifbeginn_entry.delete(0, tk.END)
        self.tarifbeginn_entry.insert(0, tarifdaten["tarifbeginn"])
        self.tarifende_entry.delete(0, tk.END)
        self.tarifende_entry.insert(0, tarifdaten["tarifende"])
        self.arbeitspreis_entry.delete(0, tk.END)
        self.arbeitspreis_entry.insert(0, tarifdaten["arbeitspreis"])
        self.grundpreis_entry.delete(0, tk.END)
        self.grundpreis_entry.insert(0, tarifdaten["grundpreis"])
        self.zählerpreis_entry.delete(0, tk.END)
        self.zählerpreis_entry.insert(0, tarifdaten["zählerpreis"])
        self.mwst_entry.delete(0, tk.END)
        self.mwst_entry.insert(0, tarifdaten["mwst"])

        def save_edit():
            self.data["tarifdaten"] = [t for t in self.data["tarifdaten"] if t["vertragskonto"] != self.app.current_contract]
            self.add_tarif()
            edit_window.destroy()

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Tarif bearbeiten")
        ttk.Button(edit_window, text="Speichern", command=save_edit).pack(pady=10)