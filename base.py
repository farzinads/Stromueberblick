<<<<<<< HEAD
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import os

PDF_DIR = "zahlungen_pdfs"
if not os.path.exists(PDF_DIR):
    os.makedirs(PDF_DIR)
=======
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

PDF_DIR = "zahlungen_pdfs"

def load_data():
    if os.path.exists("electricity_data.json"):
        with open("electricity_data.json", "r") as f:
            return json.load(f)
    return {"contracts": [], "tarifedaten": [], "ablesung": [], "zahlungen": []}

def save_data(data):
    with open("electricity_data.json", "w") as f:
        json.dump(data, f, indent=4)
>>>>>>> 1b51e8c33d9a0d94737b7d340c7f90a601d0c100
