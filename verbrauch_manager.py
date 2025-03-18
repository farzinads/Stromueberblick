from base import tk, ttk

class VerbrauchManager:
    def __init__(self, app):
        self.app = app
        self.root = app.root
        self.data = app.data
        self.current_contract = None
        self.verbrauch_tab = app.verbrauchtsmengen_tab
        self.setup_verbrauch_tab()

    def setup_verbrauch_tab(self):
        for widget in self.verbrauch_tab.winfo_children():
            widget.destroy()

        table_frame = ttk.Frame(self.verbrauch_tab, relief="solid", borderwidth=2)
        table_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.verbrauch_table = ttk.Treeview(table_frame, columns=("Zeitraum", "Zählerstand", "Verbrauch"), show="headings")
        self.verbrauch_table.heading("Zeitraum", text="Zeitraum")
        self.verbrauch_table.heading("Zählerstand", text="Zählerstand")
        self.verbrauch_table.heading("Verbrauch", text="Verbrauch")
        self.verbrauch_table.column("Zeitraum", width=150, anchor="center")
        self.verbrauch_table.column("Zählerstand", width=120, anchor="center")
        self.verbrauch_table.column("Verbrauch", width=120, anchor="center")
        self.verbrauch_table.pack(fill="both", expand=True)

        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        self.verbrauch_table.tag_configure("oddrow", background="#d3d3d3")
        self.verbrauch_table.tag_configure("evenrow", background="#ffffff")

        self.update_verbrauch_table()

    def update_verbrauch_table(self):
        self.verbrauch_table.delete(*self.verbrauch_table.get_children())
        if "ablesungen" in self.data and self.app.current_contract:
            ablesungen = [a for a in self.data["ablesungen"] if a["vertragskonto"] == self.app.current_contract]
            ablesungen.sort(key=lambda x: x["ablesungsdatum"])
            for i, ablesung in enumerate(ablesungen):
                zeitraum = ablesung["ablesungsdatum"]
                if i > 0:
                    zeitraum = f"{ablesungen[i-1]['ablesungsdatum']} - {ablesung['ablesungsdatum']}"
                zählerstand = f"HT: {ablesung['zählerstand_ht']} NT: {ablesung['zählerstand_nt']}"
                verbrauch = "N/A"
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                self.verbrauch_table.insert("", "end", values=(zeitraum, zählerstand, verbrauch), tags=(tag,))