from base import tk, ttk, messagebox, DateEntry

class TarifManager:
    def __init__(self, app):
        self.app = app
        self.root = app.root
        self.data = app.data
        self.current_contract = app.current_contract
        self.tarifedaten_tab = app.tarifedaten_tab
        self.setup_tarifedaten_tab()

    def setup_tarifedaten_tab(self):
        ttk.Label(self.tarifedaten_tab, text="Hier kommen die Tarifdaten").pack(pady=20)

    def update_tarif_table(self):
        pass  # بعداً جدول تعرفه‌ها رو اضافه می‌کنیم