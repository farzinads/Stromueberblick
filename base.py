import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import os

PDF_DIR = "zahlungen_pdfs"
if not os.path.exists(PDF_DIR):
    os.makedirs(PDF_DIR)