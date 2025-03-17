<<<<<<< HEAD
import tkinter as tk
from tkinter import ttk
import json
import os
from contract_manager import ContractManager

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Electricity Tracker")
        self.root.geometry("1000x650")
        self.data = self.load_data()
        self.current_contract = None

        # فریم‌ها
        self.contract_frame = ttk.Frame(self.root)
        self.tabs_frame = ttk.Frame(self.root)
        
        # ContractManager
        self.contract_manager = ContractManager(self)
        
        # شروع با صفحه قراردادها
        self.show_contract_page()

    def load_data(self):
        try:
            with open("electricity_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"contracts": [], "ablesungen": [], "tarife": [], "rechnungen": [], "zahlungen": []}

    def save_data(self):
        with open("electricity_data.json", "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def show_contract_page(self):
        self.tabs_frame.pack_forget()
        self.contract_frame.pack(fill="both", expand=True)

    def show_tabs_page(self):
        self.contract_frame.pack_forget()
        self.tabs_frame.pack(fill="both", expand=True)
        self.contract_manager.update_tabs()  # به‌روزرسانی تب‌ها

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
=======
import tkinter as tk
from app import ElectricityTrackerApp
from contract_manager import ContractManager
from details_tabs import DetailsTabs
from tarif_manager import TarifManager
from ablesung_manager import AblesungManager
from zahlung_manager import ZahlungManager
from rechnungen_manager import RechnungenManager

class MainApp(ElectricityTrackerApp, ContractManager, DetailsTabs, TarifManager, AblesungManager, ZahlungManager, RechnungenManager):
    def __init__(self, root):
        ElectricityTrackerApp.__init__(self, root)
        
        # راه‌اندازی صفحات و تب‌ها
        self.setup_contract_page()  # از ContractManager
        self.setup_contract_details_page()  # از DetailsTabs
        self.setup_tarifedaten_tab()  # از TarifManager
        self.setup_ablesung_tab()  # از AblesungManager
        self.setup_zahlungen_tab()  # از ZahlungManager
        self.setup_energiekosten_tab()  # از ZahlungManager
        self.setup_rechnungen_tab()  # از RechnungenManager
        
        self.switch_page(self.contract_frame)

    def setup_rechnungen_tab(self):
        RechnungenManager.setup_rechnungen_tab(self)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
>>>>>>> 1b51e8c33d9a0d94737b7d340c7f90a601d0c100
    root.mainloop()