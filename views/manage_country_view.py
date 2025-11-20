import tkinter as tk
from tkinter import ttk, messagebox


class ManageCountryWindow(tk.Toplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.title("Manage Country")
        self.geometry("900x480")

        self.create_widgets()
        self.refresh_list()

    def create_widgets(self):
        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # =====================================================
        # TABLE (5 CỘT)
        # =====================================================
        columns = ("id", "name", "code", "population", "currency")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)

        headers = [
            ("id", "ID"),
            ("name", "Country Name"),
            ("code", "Code"),
            ("population", "Population"),
            ("currency", "Currency"),
        ]

        for col, text in headers:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=130, anchor="center")

        self.tree.grid(row=0, column=0, sticky="nsew")

        scroll = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scroll.set)

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # ============= FORM ================
        form = ttk.Frame(frame)
        form.grid(row=1, column=0, pady=10, sticky="w")

        # NAME
        ttk.Label(form, text="Name:").grid(row=0, column=0, sticky="e")
        self.name_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.name_var, width=30).grid(row=0, column=1, padx=5)

        # CODE
        ttk.Label(form, text="Country code:").grid(row=1, column=0, sticky="e")
        self.code_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.code_var, width=30).grid(row=1, column=1, padx=5)

        # POPULATION
        ttk.Label(form, text="Population:").grid(row=2, column=0, sticky="e")
        self.population_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.population_var, width=30).grid(row=2, column=1, padx=5)

        # CURRENCY
        ttk.Label(form, text="Currency:").grid(row=3, column=0, sticky="e")
        self.currency_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.currency_var, width=30).grid(row=3, column=1, padx=5)

        # BUTTONS
        btns = ttk.Frame(form)
        btns.grid(row=0, column=2, rowspan=4, padx=30)

        ttk.Button(btns, text="Add", command=self.on_add).pack(fill="x", pady=2)
        ttk.Button(btns, text="Update", command=self.on_update).pack(fill="x", pady=2)
        ttk.Button(btns, text="Delete", command=self.on_delete).pack(fill="x", pady=2)

        # SEARCH
        ttk.Label(form, text="Search:").grid(row=4, column=0, pady=10)
        self.search_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.search_var, width=30).grid(row=4, column=1)
        ttk.Button(form, text="Find", command=self.on_search).grid(row=4, column=2)

    # =====================================================
    # LOAD LIST
    # =====================================================
    def refresh_list(self):
        rows = self.controller.get_all_countries()
        self.tree.delete(*self.tree.get_children())
        for r in rows:
            self.tree.insert(
                "",
                "end",
                values=(r["id"], r["name"], r["country_code"], r["population"], r["currency"])
            )

    # =====================================================
    # SELECT ROW → FILL FORM
    # =====================================================
    def on_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        item = self.tree.item(sel[0])
        _id, name, code, population, currency = item["values"]

        self.name_var.set(name)
        self.code_var.set(code)
        self.population_var.set(population)
        self.currency_var.set(currency)

    def selected_id(self):
        sel = self.tree.selection()
        if not sel:
            return None
        return self.tree.item(sel[0])["values"][0]

    # =====================================================
    # CRUD
    # =====================================================
    def on_add(self):
        self.controller.add_country(
            self.name_var.get(),
            self.code_var.get(),
            self.population_var.get(),
            self.currency_var.get()
        )
        self.refresh_list()

    def on_update(self):
        cid = self.selected_id()
        if not cid:
            return messagebox.showwarning("Warning", "Select an item first")
        self.controller.update_country(
            cid,
            self.name_var.get(),
            self.code_var.get(),
            self.population_var.get(),
            self.currency_var.get()
        )
        self.refresh_list()

    def on_delete(self):
        cid = self.selected_id()
        if not cid:
            return messagebox.showwarning("Warning", "Select an item first")
        self.controller.delete_country(cid)
        self.refresh_list()

    def on_search(self):
        rows = self.controller.search_country(self.search_var.get())
        self.tree.delete(*self.tree.get_children())
        for r in rows:
            self.tree.insert(
                "",
                "end",
                values=(r["id"], r["name"], r["country_code"], r["population"], r["currency"])
            )
