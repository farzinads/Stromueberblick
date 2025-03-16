from base import tk, ttk, messagebox, DateEntry, os
import shutil

class ZahlungManager:
    def __init__(self, app):
        self.root = app.root
        self.data = app.data
        self.current_contract = app.current_contract
        self.zahlung_tab = app.zahlung_tab
        self.setup_zahlung_tab()

    def setup_zahlung_tab(self):
        zahlung_frame = ttk.Frame(self.zahlung_tab)
        zahlung_frame.place(x=10, y=10)

        ttk.Label(zahlung_frame, text="Zahlungsdatum:").grid(row=0, column=0, pady=5, sticky="w")
        self.zahlungsdatum = DateEntry(zahlung_frame, date_pattern="dd.mm.yyyy")
        self.zahlungsdatum.grid(row=0, column=1, pady=5)

        ttk.Label(zahlung_frame, text="Betrag (€):").grid(row=1, column=0, pady=5, sticky="w")
        self.betrag = ttk.Entry(zahlung_frame)
        self.betrag.grid(row=1, column=1, pady=5)

        ttk.Button(zahlung_frame, text="PDF hochladen", command=self.upload_pdf).grid(row=2, column=0, pady=5)
        self.pdf_label = ttk.Label(zahlung_frame, text="Kein PDF ausgewählt")
        self.pdf_label.grid(row=2, column=1, pady=5)

        ttk.Button(zahlung_frame, text="Speichern", command=self.save_zahlung).grid(row=3, column=0, columnspan=2, pady=10)

        table_frame_zahlung = ttk.Frame(self.zahlung_tab, relief="solid", borderwidth=2)
        table_frame_zahlung.place(x=10, y=130, width=960, height=520)

        self.zahlung_table = ttk.Treeview(table_frame_zahlung, columns=("Zahlungsdatum", "Betrag", "PDF"), show="headings")
        self.zahlung_table.heading("Zahlungsdatum", text="Zahlungsdatum")
        self.zahlung_table.heading("Betrag", text="Betrag (€)")
        self.zahlung_table.heading("PDF", text="PDF")
        self.zahlung_table.column("Zahlungsdatum", width=200, anchor="center")
        self.zahlung_table.column("Betrag", width=150, anchor="center")
        self.zahlung_table.column("PDF", width=150, anchor="center")

        scrollbar_zahlung = ttk.Scrollbar(table_frame_zahlung, orient="vertical", command=self.zahlung_table.yview)
        self.zahlung_table.configure(yscrollcommand=scrollbar_zahlung.set)
        scrollbar_zahlung.pack(side="right", fill="y")
        self.zahlung_table.pack(fill="both", expand=True)

        self.update_zahlung_table()

    def upload_pdf(self):
        pdf_path = tk.filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if pdf_path:
            self.current_pdf_path = pdf_path
            self.pdf_label.config(text=os.path.basename(pdf_path))

    def save_zahlung(self):
        if not self.current_contract:
            messagebox.showerror("Fehler", "Kein Vertrag ausgewählt!")
            return
        zahlungsdatum = self.zahlungsdatum.get()
        betrag = self.betrag.get()
        if not all([zahlungsdatum, betrag]):
            messagebox.showerror("Fehler", "Zahlungsdatum und Betrag müssen ausgefüllت sein!")
            return
        try:
            float(betrag)
        except ValueError:
            messagebox.showerror("Fehler", "Betrag muss numerisch sein!")
            return
        pdf_path = None
        if hasattr(self, 'current_pdf_path') and self.current_pdf_path:
            pdf_filename = f"Zahlung_{self.current_contract}_{zahlungsdatum.replace('.', '_')}_{os.path.basename(self.current_pdf_path)}"
            pdf_path = os.path.join("zahlungen_pdfs", pdf_filename)
            shutil.copy(self.current_pdf_path, pdf_path)
        zahlung = {
            "vertragskonto": self.current_contract,
            "zahlungsdatum": zahlungsdatum,
            "betrag": betrag,
            "pdf_path": pdf_path if pdf_path else "-"
        }
        if "zahlungen" not in self.data:
            self.data["zahlungen"] = []
        self.data["zahlungen"].append(zahlung)
        self.app.save_data()  # تغییر به self.app.save_data()
        messagebox.showinfo("Erfolg", "Zahlung wurde gespeichert!")
        self.clear_zahlung_entries()
        self.update_zahlung_table()

    def update_zahlung_table(self):
        self.zahlung_table.delete(*self.zahlung_table.get_children())
        if self.current_contract and "zahlungen" in self.data:
            for zahlung in self.data["zahlungen"]:
                if zahlung["vertragskonto"] == self.current_contract:
                    pdf_status = "Anzeigen" if zahlung["pdf_path"] != "-" else "-"
                    self.zahlung_table.insert("", "end", values=(zahlung["zahlungsdatum"], zahlung["betrag"], pdf_status))

    def clear_zahlung_entries(self):
        self.zahlungsdatum.delete(0, tk.END)
        self.betrag.delete(0, tk.END)
        self.pdf_label.config(text="Kein PDF ausgewählt")
        if hasattr(self, 'current_pdf_path'):
            del self.current_pdf_path