import tkinter as tk
from tkinter import ttk, messagebox
from base import load_data, save_data
from contract_manager import ContractManager
from tarif_manager import TarifManager
from ablesung_manager import AblesungManager
from verbrauch_manager import VerbrauchManager

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

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_tabs_frame(self):
        info_frame = ttk.Frame(self.tabs_frame)
        info_frame.pack(fill="x", padx=10, pady=5)
        
        style = ttk.Style()
        style.configure("Green.TLabel", foreground="#006400", font=("Arial", 12))
        
        self.contract_label = ttk.Label(info_frame, text="Vertragskontonummer: ", style="Green.TLabel")
        self.contract_label.pack(side="left")
        self.vertragstyp_label = ttk.Label(info_frame, text="Vertragstyp: ", style="Green.TLabel")
        self.vertragstyp_label.pack(side="left", padx=50)

        ttk.Button(info_frame, text="Zurück", command=self.show_contracts).pack(side="right")

        self.notebook = ttk.Notebook(self.tabs_frame)
        self.tarifedaten_tab = ttk.Frame(self.notebook)
        self.ablesung_tab = ttk.Frame(self.notebook)
        self.verbrauchtsmengen_tab = ttk.Frame(self.notebook)
        self.energiekosten_tab = ttk.Frame(self.notebook)
        self.zahlungen_tab = ttk.Frame(self.notebook)
        self.rechnungen_tab = ttk.Frame(self.notebook)
        self.raten_tab = ttk.Frame(self.notebook)
        self.offene_beträge_tab = ttk.Frame(self.notebook)
        self.diagramm_tab = ttk.Frame(self.notebook)

        style.configure("TNotebook", tabmargins=[15, 0, 15, 0])
        style.configure("TNotebook.Tab", foreground="#8B0000", relief="raised", padding=[5, 2])
        style.map("TNotebook.Tab", foreground=[("selected", "#0000FF")])

        self.notebook.add(self.tarifedaten_tab, text="Tarifdaten")
        self.notebook.add(self.ablesung_tab, text="Ablesung")
        self.notebook.add(self.verbrauchtsmengen_tab, text="Verbrauchtsmengen")
        self.notebook.add(self.energiekosten_tab, text="Energiekosten")
        self.notebook.add(self.zahlungen_tab, text="Zahlungen")
        self.notebook.add(self.rechnungen_tab, text="Rechnungen")
        self.notebook.add(self.raten_tab, text="Raten")
        self.notebook.add(self.offene_beträge_tab, text="Aktuell offene Beträge")
        self.notebook.add(self.diagramm_tab, text="Diagramm")

        self.notebook.pack(fill="both", expand=True)

        self.tarif_manager = TarifManager(self)
        self.ablesung_manager = AblesungManager(self)
        self.verbrauch_manager = VerbrauchManager(self)

    def save_data(self):
        save_data(self.data)

    def show_tabs(self):
        if not self.current_contract:
            messagebox.showerror("Fehler", "Kein Vertrag ausgewählt! Bitte einen Vertrag auswählen.")
            return
        print(f"Showing tabs for contract: {self.current_contract}")  # دیباگ
        self.contract_frame.pack_forget()
        self.tabs_frame.pack(fill="both", expand=True)
        for contract in self.data["contracts"]:
            if contract["vertragskonto"] == self.current_contract:
                self.contract_label.config(text=f"Vertragskontonummer: {contract['vertragskonto']}")
                self.vertragstyp_label.config(text=f"Vertragstyp: {contract.get('vertragstyp', '')}")
                break
        self.tarif_manager.update_tarif_table()
        self.ablesung_manager.update_ablesung_table()
        self.verbrauch_manager.update_verbrauch_table()

    def show_contracts(self):
        self.tabs_frame.pack_forget()
        self.contract_frame.pack(fill="both", expand=True)
        self.contract_manager.update_contract_table()

    def on_closing(self):
        self.save_data()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = StromÜberblick(root)
    root.mainloop()