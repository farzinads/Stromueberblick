import tkinter as tk
from tkinter import ttk, messagebox
from base import load_data, save_data

class AblesungManager:
    def __init__(self, app):
        self.app = app
        self.root = app.root
        self.data = app.data
        self.ablesung_tab = app.ablesung_tab
        self.setup_ablesung_tab()

    def setup_ablesung_tab(self):
        for widget in self.ablesung_tab.winfo_children():
            widget.destroy()

        input_frame = ttk.LabelFrame(self.ablesung_tab, text="Ablesung hinzufügen", relief="solid", borderwidth=2)
        input_frame.pack(pady=10, padx=20, fill="x")

        ttk.Label(input_frame, text="Ablesungsdatum (dd.mm.yyyy):").grid(row=0, column=0, padx=5, pady=5)
        self.ablesungsdatum_entry = ttk.Entry(input_frame)
        self.ablesungsdatum_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Zählerstand HT:").grid(row=1, column=0, padx=5, pady=5)
        self.zählerstand_ht_entry = ttk.Entry(input_frame)
        self.zählerstand_ht_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Zählerstand NT:").grid(row=2, column=0, padx=5, pady=5)
        self.zählerstand_nt_entry = ttk.Entry(input_frame)
        self.zählerstand_nt_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(input_frame, text="Hinzufügen", command=self.add_ablesung).grid(row=3, column=0, columnspan=2, pady=10)

        table_frame = ttk.Frame(self.ablesung_tab, relief="solid", borderwidth=2)
        table_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.ablesung_table = ttk.Treeview(table_frame, columns=("Ablesungsdatum", "Zählerstand HT", "Zählerstand NT"), show="headings")
        self.ablesung_table.heading("Ablesungsdatum", text="Ablesungsdatum")
        self.ablesung_table.heading("Zählerstand HT", text="Zählerstand HT")
        self.ablesung_table.heading("Zählerstand NT", text="Zählerstand NT")
        self.ablesung_table.column("Ablesungsdatum", width=150, minwidth=150, stretch=False)
        self.ablesung_table.column("Zählerstand HT", width=150, minwidth=150, stretch=False)
        self.ablesung_table.column("Zählerstand NT", width=150, minwidth=150, stretch=False)
        self.ablesung_table.pack(fill="both", expand=True)

        style = ttk.Style()
        style.configure("Treeview", rowheight=25, font=("Arial", 10))  # فونت 10
        style.configure("Treeview.Heading", font="Arial 10 bold")
        self.ablesung_table.tag_configure("oddrow", background="#d3d3d3")
        self.ablesung_table.tag_configure("evenrow", background="#ffffff")

        self.ablesung_table.bind("<Double-1>", self.edit_ablesung)
        self.update_ablesung_table()

    def add_ablesung(self):
        ablesungsdatum = self.ablesungsdatum_entry.get()
        zählerstand_ht = self.zählerstand_ht_entry.get()
        zählerstand_nt = self.zählerstand_nt_entry.get()

        if not all([ablesungsdatum, zählerstand_ht, zählerstand_nt]):
            messagebox.showerror("Fehler", "Alle Felder sind Pflichtfelder!")
            return

        if "ablesungen" not in self.data:
            self.data["ablesungen"] = []

        self.data["ablesungen"].append({
            "vertragskonto": self.app.current_contract,
            "ablesungsdatum": ablesungsdatum,
            "zählerstand_ht": zählerstand_ht,
            "zählerstand_nt": zählerstand_nt
        })
        self.app.save_data()
        self.update_ablesung_table()
        self.app.refresh_all_tabs()  # آپدیت خودکار

    def update_ablesung_table(self):
        self.ablesung_table.delete(*self.ablesung_table.get_children())
        if "ablesungen" not in self.data or not self.app.current_contract:
            return
        ablesungen = [a for a in self.data["ablesungen"] if a["vertragskonto"] == self.app.current_contract]
        for i, ablesung in enumerate(ablesungen):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.ablesung_table.insert("", "end", values=(
                ablesung["ablesungsdatum"],
                ablesung["zählerstand_ht"],
                ablesung["zählerstand_nt"]
            ), tags=(tag,))

    def edit_ablesung(self, event):
        item = self.ablesung_table.selection()
        if not item:
            return
        index = self.ablesung_table.index(item[0])
        ablesungen = [a for a in self.data["ablesungen"] if a["vertragskonto"] == self.app.current_contract][index]

        self.ablesungsdatum_entry.delete(0, tk.END)
        self.ablesungsdatum_entry.insert(0, ablesungen["ablesungsdatum"])
        self.zählerstand_ht_entry.delete(0, tk.END)
        self.zählerstand_ht_entry.insert(0, ablesungen["zählerstand_ht"])
        self.zählerstand_nt_entry.delete(0, tk.END)
        self.zählerstand_nt_entry.insert(0, ablesungen["zählerstand_nt"])

        def save_edit():
            self.data["ablesungen"] = [a for a in self.data["ablesungen"] if a["vertragskonto"] != self.app.current_contract]
            self.add_ablesung()
            edit_window.destroy()

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Ablesung bearbeiten")
        ttk.Button(edit_window, text="Speichern", command=save_edit).pack(pady=10)