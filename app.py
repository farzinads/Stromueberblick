import tkinter as tk
from tkinter import ttk
from base import load_data, save_data
from contract_manager import ContractManager

class StromÜberblick:
    def __init__(self, root):
        self.root = root
        self.root.title("Stromüberblick")
        self.root.geometry("1000x700")
        self.data = load_data()
        self.current_contract = None

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.contract_manager = ContractManager(self)

    def save_data(self):
        save_data(self.data)

if __name__ == "__main__":
    root = tk.Tk()
    app = StromÜberblick(root)
    root.mainloop()