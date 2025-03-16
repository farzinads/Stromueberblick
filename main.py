import tkinter as tk
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