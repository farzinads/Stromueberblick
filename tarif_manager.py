from base import tk, ttk, messagebox, DateEntry, os

class TarifManager:
    def __init__(self, app):
        self.root = app.root
        self.app = app
        self.data = app.data
        self.current_contract = app.current_contract
        self.tarif_tab = app.tarif_tab
        self.setup_tarif_tab()

    def setup_tarif_tab(self):
        tarif_frame = ttk.Frame(self.tarif_tab)
        tarif_frame.place(x=10, y=10)

        # بازه زمانی با فاصله‌های مشخص
        ttk.Label(tarif_frame, text="Zeitraum:").grid(row=0, column=0, pady=5, sticky="w")
        ttk.Label(tarif_frame, text="Von:").grid(row=0, column=1, pady=5, padx=(0, 10), sticky="w")  # 10 پیکسل از ورودی
        self.von_datum = DateEntry(tarif_frame, date_pattern="dd.mm.yyyy")
        self.von_datum.grid(row=0, column=2, pady=5)
        ttk.Label(tarif_frame, text="Bis:").grid(row=0, column=3, pady=5, padx=(40, 10), sticky="w")  # 40 از Von، 10 از Bis
        self.bis_datum = DateEntry(tarif_frame, date_pattern="dd.mm.yyyy")
        self.bis_datum.grid(row=0, column=4, pady=5)

        # فیلدها با فاصله‌های مشخص
        ttk.Label(tarif_frame, text="Arbeitspreis HT (Ct/kWh):").grid(row=1, column=0, pady=5, sticky="w")
        self.arbeitspreis_ht = ttk.Entry(tarif_frame)
        self.arbeitspreis_ht.grid(row=1, column=1, pady=5, padx=(0, 10))  # 10 پیکسل از برچسب
        ttk.Label(tarif_frame, text="ID:").grid(row=1, column=2, pady=5, padx=(40, 10), sticky="w")  # 40 از ورودی قبلی
        self.arbeitspreis_ht_id = ttk.Entry(tarif_frame, width=10)
        self.arbeitspreis_ht_id.grid(row=1, column=3, pady=5)

        ttk.Label(tarif_frame, text="Arbeitspreis NT (Ct/kWh):").grid(row=2, column=0, pady=5, sticky="w")
        self.arbeitspreis_nt = ttk.Entry(tarif_frame)
        self.arbeitspreis_nt.grid(row=2, column=1, pady=5, padx=(0, 10))
        ttk.Label(tarif_frame, text="ID:").grid(row=2, column=2, pady=5, padx=(40, 10), sticky="w")
        self.arbeitspreis_nt_id = ttk.Entry(tarif_frame, width=10)
        self.arbeitspreis_nt_id.grid(row=2, column=3, pady=5)

        ttk.Label(tarif_frame, text="Grundpreis (€/Jahr):").grid(row=3, column=0, pady=5, sticky="w")
        self.grundpreis = ttk.Entry(tarif_frame)
        self.grundpreis.grid(row=3, column=1, pady=5, padx=(0, 10))
        ttk.Label(tarif_frame, text="ID:").grid(row=3, column=2, pady=5, padx=(40, 10), sticky="w")
        self.grundpreis_id = ttk.Entry(tarif_frame, width=10)
        self.grundpreis_id.grid(row=3, column=3, pady=5)

        ttk.Label(tarif_frame, text="Zählerkosten (€/Jahr):").grid(row=4, column=0, pady=5, sticky="w")
        self.zählerkosten = ttk.Entry(tarif_frame)
        self.zählerkosten.grid(row=4, column=1, pady=5, padx=(0, 10))
        ttk.Label(tarif_frame, text="ID:").grid(row=4, column=2, pady=5, padx=(40, 10), sticky="w")
        self.zählerkosten_id = ttk.Entry(tarif_frame, width=10)
        self.zählerkosten_id.grid(row=4, column=3, pady=5)

        # دکمه Speichern
        ttk.Button(tarif_frame, text="Speichern", command=self.save_tarif).grid(row=5, column=0, columnspan=4, pady=10)

        # جدول
        table_frame = ttk.Frame(self.tarif_tab, relief="solid", borderwidth=2)
        table_frame.place(x=10, y=170, width=960, height=480)

        self.tarif_table = ttk.Treeview(table_frame, columns=("Von", "Bis", "Arbeitspreis HT", "Arbeitspreis NT", "Grundpreis", "Zählerkosten"), show="headings")
        self.tarif_table.heading("Von", text="Von")
        self.tarif_table.heading("Bis", text="Bis")
        self.tarif_table.heading("Arbeitspreis HT", text="Arbeitspreis HT (Ct/kWh)")
        self.tarif_table.heading("Arbeitspreis NT", text="Arbeitspreis NT (Ct/kWh)")
        self.tarif_table.heading("Grundpreis", text="Grundpreis (€/Jahr)")
        self.tarif_table.heading("Zählerkosten", text="Zählerkosten (€/Jahr)")
        self.tarif_table.column("Von", width=100, anchor="center")
        self.tarif_table.column("Bis", width=100, anchor="center")
        self.tarif_table.column("Arbeitspreis HT", width=150, anchor="center")
        self.tarif_table.column("Arbeitspreis NT", width=150, anchor="center")
        self.tarif_table.column("Grundpreis", width=150, anchor="center")
        self.tarif_table.column("Zählerkosten", width=150, anchor="center")
        self.tarif_table.pack(fill="both", expand=True)

        self.update_tarif_table()

    def save_tarif(self):
        if not self.current_contract:
            messagebox.showerror("Fehler", "Kein Vertrag ausgewählt!")
            return
        von_datum = self.von_datum.get()
        bis_datum = self.bis_datum.get()
        arbeitspreis_ht = self.arbeitspreis_ht.get()
        arbeitspreis_nt = self.arbeitspreis_nt.get()
        grundpreis = self.grundpreis.get()
        zählerkosten = self.zählerkosten.get()
        arbeitspreis_ht_id = self.arbeitspreis_ht_id.get()
        arbeitspreis_nt_id = self.arbeitspreis_nt_id.get()
        grundpreis_id = self.grundpreis_id.get()
        zählerkosten_id = self.zählerkosten_id.get()

        if not all([von_datum, bis_datum, arbeitspreis_ht, arbeitspreis_nt, grundpreis, zählerkosten,
                    arbeitspreis_ht_id, arbeitspreis_nt_id, grundpreis_id, zählerkosten_id]):
            messagebox.showerror("Fehler", "Alle Felder müssen ausgefüllت sein!")
            return
        try:
            arbeitspreis_ht = float(arbeitspreis_ht)
            arbeitspreis_nt = float(arbeitspreis_nt)
            grundpreis = float(grundpreis)
            zählerkosten = float(zählerkosten)
        except ValueError:
            messagebox.showerror("Fehler", "Numerische Werte erforderlich!")
            return
        tarif = {
            "vertragskonto": self.current_contract,
            "von_datum": von_datum,
            "bis_datum": bis_datum,
            "arbeitspreis_ht": arbeitspreis_ht,
            "arbeitspreis_nt": arbeitspreis_nt,
            "grundpreis": grundpreis,
            "zählerkosten": zählerkosten,
            "arbeitspreis_ht_id": arbeitspreis_ht_id,
            "arbeitspreis_nt_id": arbeitspreis_nt_id,
            "grundpreis_id": grundpreis_id,
            "zählerkosten_id": zählerkosten_id
        }
        if "tarife" not in self.data:
            self.data["tarife"] = []
        self.data["tarife"].append(tarif)
        self.app.save_data()
        messagebox.showinfo("Erfolg", "Tarif wurde gespeichert!")
        self.clear_tarif_entries()
        self.update_tarif_table()

    def update_tarif_table(self):
        self.current_contract = self.app.current_contract
        self.tarif_table.delete(*self.tarif_table.get_children())
        if self.current_contract and "tarife" in self.data:
            for tarif in self.data["tarife"]:
                if tarif["vertragskonto"] == self.current_contract:
                    self.tarif_table.insert("", "end", values=(
                        tarif["von_datum"],
                        tarif["bis_datum"],
                        f"{tarif['arbeitspreis_ht']} ({tarif['arbeitspreis_ht_id']})",
                        f"{tarif['arbeitspreis_nt']} ({tarif['arbeitspreis_nt_id']})",
                        f"{tarif['grundpreis']} ({tarif['grundpreis_id']})",
                        f"{tarif['zählerkosten']} ({tarif['zählerkosten_id']})"
                    ))

    def clear_tarif_entries(self):
        self.von_datum.delete(0, tk.END)
        self.bis_datum.delete(0, tk.END)
        self.arbeitspreis_ht.delete(0, tk.END)
        self.arbeitspreis_nt.delete(0, tk.END)
        self.grundpreis.delete(0, tk.END)
        self.zählerkosten.delete(0, tk.END)
        self.arbeitspreis_ht_id.delete(0, tk.END)
        self.arbeitspreis_nt_id.delete(0, tk.END)
        self.grundpreis_id.delete(0, tk.END)
        self.zählerkosten_id.delete(0, tk.END)