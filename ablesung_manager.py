import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
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

        self.ablesung_save_button = ttk.Button(input_frame, text="Speichern", command=self.save_ablesung)
        self.ablesung_save_button.grid(row=3, column=1, pady=5, sticky="w")
        self.ablesung_save_button.configure(style="Red.TButton")
        style = ttk.Style()
        style.configure("Red.TButton", foreground="red", font=("Arial", 10, "bold"))

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

        style.configure("Treeview", rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        self.ablesung_table.tag_configure("oddrow", background="#d3d3d3")
        self.ablesung_table.tag_configure("evenrow", background="#ffffff")

        self.ablesung_table.bind("<Button-3>", self.show_context_menu)
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Bearbeiten", command=self.edit_ablesung)
        self.context_menu.add_command(label="Löschen", command=self.delete_ablesung)

        self.update_ablesung_table()

    def save_ablesung(self):
        if not self.app.current_contract:
            messagebox.showerror("Fehler", "Kein Vertrag ausgewählt!")
            return
        ablesung = {
            "vertragskonto": self.app.current_contract,
            "ablesungsdatum": self.ablesungsdatum.get(),
            "zählerstand_ht": self.zählerstand_ht.get().strip(),
            "zählerstand_nt": self.zählerstand_nt.get().strip()
        }
        if not all([ablesung["ablesungsdatum"], ablesung["zählerstand_ht"]]):
            messagebox.showerror("Fehler", "Ablesungsdatum und Zählerstand HT dürfen nicht leer sein!")
            return
        if "ablesungen" not in self.data:
            self.data["ablesungen"] = []
        self.data["ablesungen"].append(ablesung)
        self.app.save_data()
        self.clear_ablesung_entries()
        self.update_ablesung_table()

    def clear_ablesung_entries(self):
        self.ablesungsdatum.set_date("01.01.2025")
        self.zählerstand_ht.delete(0, tk.END)
        self.zählerstand_nt.delete(0, tk.END)

    def update_ablesung_table(self):
        self.ablesung_table.delete(*self.ablesung_table.get_children())
        if "ablesungen" in self.data and self.app.current_contract:
            for i, ablesung in enumerate(self.data["ablesungen"]):
                if ablesung["vertragskonto"] == self.app.current_contract:
                    tag = "evenrow" if i % 2 == 0 else "oddrow"
                    self.ablesung_table.insert("", "end", values=(
                        ablesung["ablesungsdatum"],
                        ablesung["zählerstand_ht"],
                        ablesung["zählerstand_nt"]
                    ), tags=(tag,))

    def show_context_menu(self, event):
        item = self.ablesung_table.identify_row(event.y)
        if item:
            self.ablesung_table.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def edit_ablesung(self):
        item = self.ablesung_table.selection()
        if not item:
            return
        values = self.ablesung_table.item(item, "values")
        for ablesung in self.data["ablesungen"]:
            if ablesung["vertragskonto"] == self.app.current_contract and ablesung["ablesungsdatum"] == values[0]:
                self.ablesungsdatum.set_date(ablesung["ablesungsdatum"])
                self.zählerstand_ht.delete(0, tk.END)
                self.zählerstand_ht.insert(0, ablesung["zählerstand_ht"])
                self.zählerstand_nt.delete(0, tk.END)
                self.zählerstand_nt.insert(0, ablesung["zählerstand_nt"])
                self.data["ablesungen"].remove(ablesung)
                self.update_ablesung_table()
                self.ablesung_save_button.configure(text="Aktualisieren", command=self.update_ablesung)
                break

    def update_ablesung(self):
        self.save_ablesung()
        self.ablesung_save_button.configure(text="Speichern", command=self.save_ablesung)

    def delete_ablesung(self):
        item = self.ablesung_table.selection()
        if not item:
            return
        values = self.ablesung_table.item(item, "values")
        if messagebox.askyesno("Bestätigung", f"Möchten Sie den Eintrag {values[0]} löschen?"):
            for i, ablesung in enumerate(self.data["ablesungen"]):
                if ablesung["vertragskonto"] == self.app.current_contract and ablesung["ablesungsdatum"] == values[0]:
                    del self.data["ablesungen"][i]
                    self.app.save_data()
                    self.update_ablesung_table()
                    messagebox.showinfo("Erfolg", f"Eintrag {values[0]} wurde gelöscht!")
                    break