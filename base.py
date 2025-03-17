import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import os
import json

PDF_DIR = "pdfs"
if not os.path.exists(PDF_DIR):
    os.makedirs(PDF_DIR)

def load_data():
    try:
        with open("strom_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"contracts": [], "tarife": [], "ablesungen": [], "zahlungen": [], "rechnungen": []}

def save_data(data):
    with open("strom_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)