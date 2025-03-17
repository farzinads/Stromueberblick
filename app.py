import tkinter as tk
from tkinter import ttk
from base import load_data, save_data
from contract_manager import ContractManager
from tarif_manager import TarifManager

class StromÜberblick:
    def __init__(self, root):
        self.root = root
        self.root.title("Stromüberblick")
        self.root.geometry("1000x700")
        self.data = load_data()
        self.current_contract = None

        self.contract_frame = ttk.Frame(self.root)
        self.tabs_frame = ttk.Frame(self.root)

        self.contract_frame.pack(fill="both", expand=True)

        self.contract_manager = ContractManager(self)
        self.setup_tabs_frame()

    def setup_tabs_frame(self):
        # اطلاعات قرارداد در بالای صفحه
        info_frame = ttk.Frame(self.tabs_frame)
        info_frame.pack(fill="x", padx=10, pady=5)
        
        self.contract_label = ttk.Label(info_frame, text="Vertragskontonummer: ")
        self.contract_label.pack(side="left")
        self.vertragstyp_label = ttk.Label(info_frame, text="Vertragstyp: ")
        self.vertragstyp_label.pack(side="left", padx=10)

        # دکمه Zurück
        ttk.Button(info_frame, text="Zurück", command=self.show_contracts).pack(side="right")

        # تب‌ها
        self.notebook = ttk.Notebook(self.tabs_frame)
        self.tarifedaten_tab = ttk.Frame(self.notebook)
        self.ablesung_tab = ttk.Frame(self.notebook)
        self.energiekosten_tab = ttk.Frame(self.notebook)
        self.zahlungen_tab = ttk.Frame(self.notebook)
        self.rechnungen_tab = ttk.Frame(self.notebook)
        self.raten_tab = ttk.Frame(self.notebook)
        self.offene_beträge_tab = ttk.Frame(self.notebook)
        self.diagramm_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.tarifedaten_tab, text="Tarifdaten")
        self.notebook.add(self.ablesung_tab, text="Ablesung")
        self.notebook.add(self.energiekosten_tab, text="Energiekosten")
        self.notebook.add(self.zahlungen_tab, text="Zahlungen")
        self.notebook.add(self.rechnungen_tab, text="Rechnungen")
        self.notebook.add(self.raten_tab, text="Raten")
        self.notebook.add(self.offene_beträge_tab, text="Aktuell offene Beträge")
        self.notebook.add(self.diagramm_tab, text="Diagramm")

        self.notebook.pack(fill="both", expand=True)

        self.tarif_manager = TarifManager(self)

    def save_data(self):
        save_data(self.data)

    def show_tabs(self):
        self.contract_frame.pack_forget()
        self.tabs_frame.pack(fill="both", expand=True)
        # به‌روزرسانی اطلاعات قرارداد
        for contract in self.data["contracts"]:
            if contract["vertragskonto"] == self.current_contract:
                self.contract_label.config(text=f"Vertragskontonummer: {contract['vertragskonto']}")
                self.vertragstyp_label.config(text=f"Vertragstyp: {contract.get('vertragstyp', '')}")
                break
        self.tarif_manager.update_tarif_table()

    def show_contracts(self):
        self.tabs_frame.pack_forget()
        self.contract_frame.pack(fill="both", expand=True)
        self.contract_manager.update_contract_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = StromÜberblick(root)
    root.mainloop()