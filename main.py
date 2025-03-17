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
    root.mainloop()