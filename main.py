import tkinter as tk
from tkinter import ttk
import json
import os
from contract_manager import ContractManager
from ablesung_manager import AblesungManager
from tarif_manager import TarifManager
from rechnungen_manager import RechnungenManager
from zahlung_manager import ZahlungManager
from details_tabs import DetailsTabs

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Electricity Tracker")
        self.current_contract = None

        # بارگذاری داده‌ها
        self.data = self.load_data()

        # ساخت Notebook برای تب‌ها
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # تعریف تب‌ها
        self.contract_tab = ttk.Frame(self.notebook)
        self.ablesung_tab = ttk.Frame(self.notebook)
        self.tarif_tab = ttk.Frame(self.notebook)
        self.rechnungen_tab = ttk.Frame(self.notebook)
        self.zahlung_tab = ttk.Frame(self.notebook)
        self.details_tab = ttk.Frame(self.notebook)

        # اضافه کردن تب‌ها به Notebook
        self.notebook.add(self.contract_tab, text="Verträge")
        self.notebook.add(self.ablesung_tab, text="Energiekosten")
        self.notebook.add(self.tarif_tab, text="Tarife")
        self.notebook.add(self.rechnungen_tab, text="Rechnungen")
        self.notebook.add(self.zahlung_tab, text="Zahlungen")
        self.notebook.add(self.details_tab, text="Details")

        # تعریف مدیرها و راه‌اندازی تب‌ها
        self.contract_manager = ContractManager(self)
        self.ablesung_manager = AblesungManager(self)
        self.tarif_manager = TarifManager(self)
        self.rechnungen_manager = RechnungenManager(self)
        self.zahlung_manager = ZahlungManager(self)
        self.details_tabs = DetailsTabs(self)

        # فراخوانی توابع راه‌اندازی تب‌ها
        self.contract_manager.setup_contract_tab()
        self.ablesung_manager.setup_ablesung_tab()
        self.tarif_manager.setup_tarif_tab()
        self.rechnungen_manager.setup_rechnungen_tab()
        self.zahlung_manager.setup_zahlung_tab()
        self.details_tabs.setup_details_tabs()

    def load_data(self):
        """بارگذاری داده‌ها از electricity_data.json"""
        try:
            with open("electricity_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_data(self):
        """ذخیره داده‌ها توی electricity_data.json"""
        with open("electricity_data.json", "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def update_all_tabs(self):
        self.contract_manager.update_contract_table()
        self.ablesung_manager.update_ablesung_table()
        self.tarif_manager.update_tarif_table()
        self.rechnungen_manager.update_rechnungen_table()
        self.zahlung_manager.update_zahlung_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()