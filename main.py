import tkinter as tk
from tkinter import ttk
import json
import os
from contract_manager import ContractManager

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Electricity Tracker")
        self.data = self.load_data()

        # فقط صفحه قراردادها رو نشون می‌دیم
        self.contract_frame = ttk.Frame(self.root)
        self.contract_frame.pack(fill="both", expand=True)
        self.contract_manager = ContractManager(self)
        self.contract_manager.setup_contract_page()

    def load_data(self):
        try:
            with open("electricity_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_data(self):
        with open("electricity_data.json", "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()