import tkinter as tk
from tkinter import ttk
from base import load_data, save_data
from contract_manager import ContractManager
from tarif_manager import TarifManager
from ablesung_manager import AblesungManager
from verbrauch_manager import VerbrauchManager

class StromÜberblick:
    def __init__(self, root):
        self.root = root
        self.root.title("Stromüberblick")
        self.root.geometry("900x600")
        self.data = load_data()
        self.current_contract = None
        self.setup_tabs_frame()

    def setup_tabs_frame(self):
        self.tabs_frame = ttk.Notebook(self.root)
        self.tabs_frame.pack(fill="both", expand=True)

        self.contract_frame = ttk.Frame(self.tabs_frame)
        self.tarifdaten_tab = ttk.Frame(self.tabs_frame)
        self.ablesung_tab = ttk.Frame(self.tabs_frame)
        self.verbrauchtsmengen_tab = ttk.Frame(self.tabs_frame)

        self.tabs_frame.add(self.contract_frame, text="Verträge")
        self.tabs_frame.add(self.tarifdaten_tab, text="Tarifdaten")
        self.tabs_frame.add(self.ablesung_tab, text="Ablesung")
        self.tabs_frame.add(self.verbrauchtsmengen_tab, text="Verbrauchtsmengen")

        self.contract_manager = ContractManager(self)
        self.tarif_manager = TarifManager(self)
        self.ablesung_manager = AblesungManager(self)
        self.verbrauch_manager = VerbrauchManager(self)

        self.tabs_frame.select(self.contract_frame)  # تب Verträge اول باز می‌شه

    def save_data(self):
        save_data(self.data)

    def show_tabs(self):
        self.contract_manager.update_contract_table()
        self.tarif_manager.update_tarif_table()
        self.ablesung_manager.update_ablesung_table()
        self.verbrauch_manager.update_verbrauch_table()
        self.tabs_frame.select(self.tarifdaten_tab)

if __name__ == "__main__":
    root = tk.Tk()
    app = StromÜberblick(root)
    root.mainloop()