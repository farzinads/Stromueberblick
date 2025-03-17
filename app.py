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

        self.contract_frame = ttk.Frame(self.root)  # صفحه قراردادها
        self.tabs_frame = ttk.Frame(self.root)      # صفحه تب‌ها

        self.contract_frame.pack(fill="both", expand=True)  # قراردادها موقع شروع نشون داده بشه

        self.contract_manager = ContractManager(self)
        self.setup_tabs_frame()

    def setup_tabs_frame(self):
        self.notebook = ttk.Notebook(self.tabs_frame)
        self.tarifedaten_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.tarifedaten_tab, text="Tarifedaten")

        self.notebook.pack(fill="both", expand=True)

        self.tarif_manager = TarifManager(self)

    def save_data(self):
        save_data(self.data)

    def show_tabs(self):
        self.contract_frame.pack_forget()
        self.tabs_frame.pack(fill="both", expand=True)
        self.tarif_manager.update_tarif_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = StromÜberblick(root)
    root.mainloop()