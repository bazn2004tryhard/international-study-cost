# views/main_view.py
import tkinter as tk
from tkinter import ttk

class MainView(tk.Frame):
    def __init__(self, master, controller, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.controller = controller
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        # Combobox chọn country
        self.country_label = ttk.Label(self, text="Country:")
        self.country_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.country_var = tk.StringVar()
        self.country_combo = ttk.Combobox(self, textvariable=self.country_var, state="readonly")
        self.country_combo.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.country_combo.bind("<<ComboboxSelected>>", self.on_country_selected)

        # Treeview hiển thị kết quả chi phí
        self.tree = ttk.Treeview(self, columns=(
            "city", "university", "program", "level", "tuition", "rent", "visa", "insurance"
        ), show="headings")

        for col, text in [
            ("city", "City"),
            ("university", "University"),
            ("program", "Program"),
            ("level", "Level"),
            ("tuition", "Tuition USD"),
            ("rent", "Rent USD"),
            ("visa", "Visa Fee"),
            ("insurance", "Insurance")
        ]:
            self.tree.heading(col, text=text)

        self.tree.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

        # layout stretch
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(3, weight=1)

    def set_countries(self, country_list):
        """country_list: [{'id':..,'name':..}, ...]"""
        self.country_combo["values"] = [c["name"] for c in country_list]

    def clear_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def populate_tree(self, rows):
        self.clear_tree()
        for row in rows:
            self.tree.insert("", "end", values=(
                row["city"],
                row["university"],
                row["program"],
                row["level"],
                row["tuition_usd"],
                row["rent_usd"],
                row["visa_fee_usd"],
                row["insurance_usd"],
            ))

    def on_country_selected(self, event):
        name = self.country_var.get()
        self.controller.on_country_changed(name)
