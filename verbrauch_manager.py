import tkinter as tk
from tkinter import ttk, messagebox
from base import load_data, save_data
from datetime import datetime

class VerbrauchManager:
    def __init__(self, app):
        self.app = app
        self.root = app.root
        self.data = app.data
        self.verbrauch_tab = app.verbrauchtsmengen_tab
        self.setup_verbrauch_tab()

    def setup_verbrauch_tab(self):
        for widget in self.verbrauch_tab.winfo_children():
            widget.destroy()

        table_frame = ttk.Frame(self.verbrauch_tab, relief="solid", borderwidth=2)
        table_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.verbrauch_table = ttk.Treeview(table_frame, columns=("Zeitraum", "Zählerstand HT", "Zählerstand NT", "Verbrauch HT", "Verbrauch NT", "Verbrauch Total"), show="headings")
        self.verbrauch_table.heading("Zeitraum", text="Zeitraum")
        self.verbrauch_table.heading("Zählerstand HT", text="Zählerstand HT")
        self.verbrauch_table.heading("Zählerstand NT", text="Zählerstand NT")
        self.verbrauch_table.heading("Verbrauch HT", text="Verbrauch HT")
        self.verbrauch_table.heading("Verbrauch NT", text="Verbrauch NT")
        self.verbrauch_table.heading("Verbrauch Total", text="Verbrauch Total")
        self.verbrauch_table.column("Zeitraum", width=150, anchor="center")
        self.verbrauch_table.column("Zählerstand HT", width=150, anchor="center")
        self.verbrauch_table.column("Zählerstand NT", width=150, anchor="center")
        self.verbrauch_table.column("Verbrauch HT", width=120, anchor="center")
        self.verbrauch_table.column("Verbrauch NT", width=120, anchor="center")
        self.verbrauch_table.column("Verbrauch Total", width=120, anchor="center")
        self.verbrauch_table.pack(fill="both", expand=True)

        style = ttk.Style()
        style.configure("Treeview", rowheight=40)  # افزایش ارتفاع برای دو خط
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        self.verbrauch_table.tag_configure("oddrow", background="#d3d3d3")
        self.verbrauch_table.tag_configure("evenrow", background="#ffffff")
        self.verbrauch_table.tag_configure("summe", background="#A9A9A9", font=("Arial", 10, "bold"))  # خاکستری ملایم

        self.verbrauch_table.bind("<Button-3>", self.show_context_menu)
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Löschen", command=self.delete_verbrauch)

        self.update_verbrauch_table()

    def update_verbrauch_table(self):
        self.verbrauch_table.delete(*self.verbrauch_table.get_children())
        if "ablesungen" not in self.data or not self.app.current_contract:
            print("No ablesungen data or current_contract not set:", self.app.current_contract)
            return
        ablesungen = [a for a in self.data["ablesungen"] if a["vertragskonto"] == self.app.current_contract]
        ablesungen.sort(key=lambda x: datetime.strptime(x["ablesungsdatum"], "%d.%m.%Y"))
        superscript_map = {
            'A': 'ᴬ', 'B': 'ᴮ', '1': '¹', '2': '²', '3': '³', '4': '⁴'
        }
        total_verbrauch = 0

        for i, ablesung in enumerate(ablesungen):
            if i == 0:
                continue
            prev_ablesung = ablesungen[i-1]
            zeitraum = f"{prev_ablesung['ablesungsdatum']} - {ablesung['ablesungsdatum']}"
            source_ht_start = prev_ablesung.get("source_ht", "A1")
            source_nt_start = prev_ablesung.get("source_nt", "A1")
            source_ht_end = ablesung.get("source_ht", "A1")
            source_nt_end = ablesung.get("source_nt", "A1")

            # فقط مقادیر با مولفه‌ها
            zählerstand_ht = f"{prev_ablesung['zählerstand_ht']}{''.join(superscript_map.get(char, char) for char in source_ht_start)}\n{ablesung['zählerstand_ht']}{''.join(superscript_map.get(char, char) for char in source_ht_end)}"
            zählerstand_nt = f"{prev_ablesung['zählerstand_nt']}{''.join(superscript_map.get(char, char) for char in source_nt_start)}\n{ablesung['zählerstand_nt']}{''.join(superscript_map.get(char, char) for char in source_nt_end)}"

            try:
                ht_start = float(prev_ablesung["zählerstand_ht"])
                ht_end = float(ablesung["zählerstand_ht"])
                nt_start = float(prev_ablesung["zählerstand_nt"])
                nt_end = float(ablesung["zählerstand_nt"])
                verbrauch_ht = ht_end - ht_start  # مقدار بیشتر - کمتر
                verbrauch_nt = nt_end - nt_start
                verbrauch_total = verbrauch_ht + verbrauch_nt
                total_verbrauch += verbrauch_total
            except ValueError:
                verbrauch_ht = verbrauch_nt = verbrauch_total = "N/A"

            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.verbrauch_table.insert("", "end", values=(
                zeitraum,
                zählerstand_ht,
                zählerstand_nt,
                verbrauch_ht,
                verbrauch_nt,
                verbrauch_total
            ), tags=(tag,))
            print(f"Added to verbrauch table: {zeitraum}")

        # اضافه کردن ردیف جمع کل
        if total_verbrauch != 0:
            self.verbrauch_table.insert("", "end", values=(
                "Summe", "", "", "", "", total_verbrauch
            ), tags=("summe",))

    def show_context_menu(self, event):
        item = self.verbrauch_table.identify_row(event.y)
        if item:
            self.verbrauch_table.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def delete_verbrauch(self):
        item = self.verbrauch_table.selection()
        if not item:
            return
        values = self.verbrauch_table.item(item, "values")
        if "-" in values[0]:
            start, end = values[0].split(" - ")
            if messagebox.askyesno("Bestätigung", f"Möchten Sie den Eintrag {values[0]} löschen?"):
                for i, ablesung in enumerate(self.data["ablesungen"]):
                    if ablesung["vertragskonto"] == self.app.current_contract and ablesung["ablesungsdatum"] == end:
                        del self.data["ablesungen"][i]
                        self.app.save_data()
                        self.update_verbrauch_table()
                        messagebox.showinfo("Erfolg", f"Eintrag {values[0]} wurde gelöscht!")
                        break