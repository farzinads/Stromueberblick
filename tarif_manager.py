from base import tk, ttk, messagebox, DateEntry

class TarifManager:
    def __init__(self, app):
        self.app = app
        self.root = app.root
        self.data = app.data
        self.current_contract = app.current_contract
        self.tarifedaten_tab = app.tarifedaten_tab
        self.setup_tarifedaten_tab()

    def setup_tarifedaten_tab(self):
        for widget in self.tarifedaten_tab.winfo_children():
            widget.destroy()

        # فرم ورودی
        input_frame = ttk.Frame(self.tarifedaten_tab)
        input_frame.pack(pady=10, padx=10, anchor="nw")

        # فیلدها و کدهای شناسایی
        ttk.Label(input_frame, text="Arbeitspreis HT (kWh):").grid(row=0, column=0, pady=5, sticky="w")
        self.arbeitspreis_ht = ttk.Entry(input_frame, width=15)
        self.arbeitspreis_ht.grid(row=0, column=1, pady=5, sticky="w")
        ttk.Label(input_frame, text="ID:").grid(row=0, column=2, pady=5, sticky="w")
        self.arbeitspreis_ht_id = ttk.Entry(input_frame, width=10)
        self.arbeitspreis_ht_id.grid(row=0, column=3, pady=5, sticky="w")

        ttk.Label(input_frame, text="Arbeitspreis NT (kWh):").grid(row=1, column=0, pady=5, sticky="w")
        self.arbeitspreis_nt = ttk.Entry(input_frame, width=15)
        self.arbeitspreis_nt.grid(row=1, column=1, pady=5, sticky="w")
        ttk.Label(input_frame, text="ID:").grid(row=1, column=2, pady=5, sticky="w")
        self.arbeitspreis_nt_id = ttk.Entry(input_frame, width=10)
        self.arbeitspreis_nt_id.grid(row=1, column=3, pady=5, sticky="w")

        ttk.Label(input_frame, text="Grundpreis (€/Jahr):").grid(row=2, column=0, pady=5, sticky="w")
        self.grundpreis = ttk.Entry(input_frame, width=15)
        self.grundpreis.grid(row=2, column=1, pady=5, sticky="w")
        ttk.Label(input_frame, text="ID:").grid(row=2, column=2, pady=5, sticky="w")
        self.grundpreis_id = ttk.Entry(input_frame, width=10)
        self.grundpreis_id.grid(row=2, column=3, pady=5, sticky="w")

        ttk.Label(input_frame, text="Zähler (€/Jahr):").grid(row=3, column=0, pady=5, sticky="w")
        self.zähler = ttk.Entry(input_frame, width=15)
        self.zähler.grid(row=3, column=1, pady=5, sticky="w")
        ttk.Label(input_frame, text="ID:").grid(row=3, column=2, pady=5, sticky="w")
        self.zähler_id = ttk.Entry(input_frame, width=10)
        self.zähler_id.grid(row=3, column=3, pady=5, sticky="w")

        # دکمه Speichern
        self.save_button = ttk.Button(input_frame, text="Speichern", command=self.save_tarif)
        self.save_button.grid(row=4, column=1, pady=5, sticky="w")
        self.save_button.configure(style="Red.TButton")
        style = ttk.Style()
        style.configure("Red.TButton", foreground="red", font=("Arial", 10, "bold"))

        # جدول
        table_frame = ttk.Frame(self.tarifedaten_tab, relief="solid", borderwidth=2)
        table_frame.pack(pady=25, padx=10, fill="both", expand=True)

        self.tarif_table = ttk.Treeview(table_frame, columns=("HT", "HT_ID", "NT", "NT_ID", "Grundpreis", "Grundpreis_ID", "Zähler", "Zähler_ID"), show="headings")
        self.tarif_table.heading("HT", text="Arbeitspreis HT")
        self.tarif_table.heading("HT_ID", text="HT ID")
        self.tarif_table.heading("NT", text="Arbeitspreis NT")
        self.tarif_table.heading("NT_ID", text="NT ID")
        self.tarif_table.heading("Grundpreis", text="Grundpreis")
        self.tarif_table.heading("Grundpreis_ID", text="Grundpreis ID")
        self.tarif_table.heading("Zähler", text="Zähler")
        self.tarif_table.heading("Zähler_ID", text="Zähler ID")
        self.tarif_table.column("HT", width=100, anchor="center")
        self.tarif_table.column("HT_ID", width=80, anchor="center")
        self.tarif_table.column("NT", width=100, anchor="center")
        self.tarif_table.column("NT_ID", width=80, anchor="center")
        self.tarif_table.column("Grundpreis", width=100, anchor="center")
        self.tarif_table.column("Grundpreis_ID", width=80, anchor="center")
        self.tarif_table.column("Zähler", width=100, anchor="center")
        self.tarif_table.column("Zähler_ID", width=80, anchor="center")
        self.tarif_table.pack(fill="both", expand=True)

        style.configure("Treeview", rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        self.tarif_table.tag_configure("oddrow", background="#d3d3d3")
        self.tarif_table.tag_configure("evenrow", background="#ffffff")

        self.update_tarif_table()

    def save_tarif(self):
        if not self.current_contract:
            messagebox.showerror("Fehler", "Kein Vertrag ausgewählt!")
            return
        tarif = {
            "vertragskonto": self.current_contract,
            "arbeitspreis_ht": self.arbeitspreis_ht.get().strip(),
            "arbeitspreis_ht_id": self.arbeitspreis_ht_id.get().strip(),
            "arbeitspreis_nt": self.arbeitspreis_nt.get().strip(),
            "arbeitspreis_nt_id": self.arbeitspreis_nt_id.get().strip(),
            "grundpreis": self.grundpreis.get().strip(),
            "grundpreis_id": self.grundpreis_id.get().strip(),
            "zähler": self.zähler.get().strip(),
            "zähler_id": self.zähler_id.get().strip()
        }
        if not all([tarif["arbeitspreis_ht"], tarif["grundpreis"]]):  # حداقل HT و Grundpreis اجباری
            messagebox.showerror("Fehler", "Arbeitspreis HT und Grundpreis dürfen nicht leer sein!")
            return
        self.data["tarife"].append(tarif)
        self.app.save_data()
        self.clear_entries()
        self.update_tarif_table()
        messagebox.showinfo("Erfolg", "Tarifdaten wurden gespeichert!")

    def clear_entries(self):
        self.arbeitspreis_ht.delete(0, tk.END)
        self.arbeitspreis_ht_id.delete(0, tk.END)
        self.arbeitspreis_nt.delete(0, tk.END)
        self.arbeitspreis_nt_id.delete(0, tk.END)
        self.grundpreis.delete(0, tk.END)
        self.grundpreis_id.delete(0, tk.END)
        self.zähler.delete(0, tk.END)
        self.zähler_id.delete(0, tk.END)

    def update_tarif_table(self):
        self.tarif_table.delete(*self.tarif_table.get_children())
        if self.current_contract and "tarife" in self.data:
            for i, tarif in enumerate(self.data["tarife"]):
                if tarif["vertragskonto"] == self.current_contract:
                    tag = "evenrow" if i % 2 == 0 else "oddrow"
                    self.tarif_table.insert("", "end", values=(
                        tarif["arbeitspreis_ht"],
                        tarif["arbeitspreis_ht_id"],
                        tarif["arbeitspreis_nt"],
                        tarif["arbeitspreis_nt_id"],
                        tarif["grundpreis"],
                        tarif["grundpreis_id"],
                        tarif["zähler"],
                        tarif["zähler_id"]
                    ), tags=(tag,))