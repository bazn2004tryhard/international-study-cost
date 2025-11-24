import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image


class ManageCountryWindow(tk.Toplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.title("Manage Country")
        self.geometry("980x540")
        self.configure(bg="white")

        self.load_icons()
        self.setup_styles()

        self.create_widgets()
        self.refresh_list()


    # ------------------------------------------------------
    # LOAD ICONS
    # ------------------------------------------------------
    def load_icons(self):
        self.add_icon = ImageTk.PhotoImage(Image.open("views/icons/add.png").resize((18, 18)))
        self.update_icon = ImageTk.PhotoImage(Image.open("views/icons/update.png").resize((18, 18)))
        self.delete_icon = ImageTk.PhotoImage(Image.open("views/icons/delete.png").resize((18, 18)))
        self.find_icon = ImageTk.PhotoImage(Image.open("views/icons/find.png").resize((18, 18)))
        self.country_icon = ImageTk.PhotoImage(Image.open("views/icons/country.png").resize((18, 18)))


    # ------------------------------------------------------
    # STYLES
    # ------------------------------------------------------
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Treeview
        style.configure(
            "Treeview",
            font=("Segoe UI", 10),
            rowheight=26,
            background="white",
            fieldbackground="white"
        )
        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            foreground="white",
            background= "#3674B5"
        )
        style.map("Treeview", background=[("selected", "#BBDEFB")])

        # Button Style
        self.btn_normal = {
            "bg": "white",
            "fg": "#3674B5",
            "activebackground": "#E3F2FD",
            "activeforeground": "#0D47A1",
            "bd": 1,
            "relief": "solid",
            "highlightthickness": 0
        }


    # ------------------------------------------------------
    # UI
    # ------------------------------------------------------
    def create_widgets(self):

        # FRAME CHÍNH
        main_frame = tk.Frame(self, bg="white")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        main_frame.grid_columnconfigure(0, weight=2)  # bảng
        main_frame.grid_columnconfigure(1, weight=1)  # form + card


        # --------------------------------------------------
        # BẢNG + TIÊU ĐỀ + VIỀN
        # --------------------------------------------------
        table_card = tk.Frame(main_frame, bg="#EAF2FF", bd=2, relief="solid")
        table_card.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 15))

        title_label = tk.Label(
            table_card,
            text="🌍 Country List",
            bg="#1E88E5",
            fg="white",
            font=("Segoe UI", 12, "bold"),
            pady=8
        )
        title_label.pack(fill="x")

        table_frame = tk.Frame(table_card, bg="white")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("id", "name", "code", "population", "currency")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=18)

        headers = [
            ("id", "ID"),
            ("name", "Country Name"),
            ("code", "Code"),
            ("population", "Population"),
            ("currency", "Currency")
        ]

        for col, text in headers:
            self.tree.heading(col, text=text)
            width = 200 if col == "name" else (60 if col == "id" else 120)
            self.tree.column(col, anchor="center", width=width)

        self.tree.pack(side="left", fill="both", expand=True)

        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scroll.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scroll.set)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Màu so le
        self.tree.tag_configure("odd", background="#FFFFFF")
        self.tree.tag_configure("even", background="#9EC3EF")

        # FIX CUỘN CHUỘT
        def _on_mousewheel(event):
            self.tree.yview_scroll(int(-1 * (event.delta / 120)), "units")
            return "break"
        self.tree.bind("<MouseWheel>", _on_mousewheel)


        # --------------------------------------------------
        # FORM (row=0, col=1)
        # --------------------------------------------------
        form_card = tk.Frame(main_frame, bg="#EAF2FF", bd=2, relief="solid")
        form_card.grid(row=0, column=1, sticky="n", pady=5)

        tk.Label(
            form_card,
            text="✏️ Country Form",
            bg="#1E88E5",
            fg="white",
            font=("Segoe UI", 12, "bold"),
            pady=8
        ).pack(fill="x")

        form_frame = tk.Frame(form_card, bg="white")
        form_frame.pack(padx=10, pady=10)

        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)

        # ---- Search ----
        tk.Label(form_frame, text="Search:", bg="white", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="e", pady=4)
        self.search_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.search_var, width=26, font=("Segoe UI", 10)).grid(row=0, column=1, pady=4, padx=5)

        tk.Button(
            form_frame, text=" Find", image=self.find_icon, compound="left",
            command=self.on_search, width=120, **self.btn_normal
        ).grid(row=1, column=0, columnspan=2, pady=10)


        # ---- Input fields ----
        self.name_var = tk.StringVar()
        self.code_var = tk.StringVar()
        self.population_var = tk.StringVar()
        self.currency_var = tk.StringVar()

        fields = [
            ("Name:", self.name_var),
            ("Country code:", self.code_var),
            ("Population:", self.population_var),
            ("Currency:", self.currency_var)
        ]

        for i, (label, var) in enumerate(fields):
            tk.Label(form_frame, text=label, bg="white", font=("Segoe UI", 10)).grid(row=i+2, column=0, sticky="e", pady=8)
            entry = tk.Entry(form_frame, textvariable=var, width=26, font=("Segoe UI", 10))
            entry.grid(row=i+2, column=1, pady=8, padx=5)

        # ---- Buttons ----
        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.grid(row=10, column=0, columnspan=2, pady=20)

        tk.Button(btn_frame, text=" Add", image=self.add_icon, compound="left",
                width=110, command=self.on_add, **self.btn_normal).pack(side="left", padx=5)

        tk.Button(btn_frame, text=" Update", image=self.update_icon, compound="left",
                width=110, command=self.on_update, **self.btn_normal).pack(side="left", padx=5)

        tk.Button(btn_frame, text=" Delete", image=self.delete_icon, compound="left",
                width=110, command=self.on_delete, **self.btn_normal).pack(side="left", padx=5)


        # --------------------------------------------------
        # CARD TỔNG SỐ COUNTRY (row=1, col=1)
        # --------------------------------------------------
        card_frame = tk.Frame(main_frame, bg="white")
        card_frame.grid(row=1, column=1, sticky="n", pady=(10, 0))

        summary_card = tk.Frame(card_frame, width=300, height=150, bd=0, relief="flat", bg = None)
        summary_card.pack()

        # ---- Background image ----
        try:
            bg_img = Image.open("views/images/country.png").resize((300, 150))
            self.card_bg = ImageTk.PhotoImage(bg_img)
            tk.Label(summary_card, image=self.card_bg, bd=0).place(x=0, y=0)
        except:
            summary_card.configure(bg="#1E88E5")
            tk.Label(summary_card, bg="#1E88E5").place(x=0, y=0, relwidth=1, relheight=1)

        # ---- Total countries ----
        try:
            total = len(self.controller.get_all_countries())
        except:
            total = 0

        tk.Label(
            summary_card,
            text=str(total),
            font=("Segoe UI", 36, "bold"),
            fg="white",
            bg="#659263"
        ).place(x=20, y=30)

        # ---- Text: Total Countries ----
        tk.Label(
            summary_card,
            text="Total Countries",
            font=("Segoe UI", 12),
            fg="white",
            bg="#659263",
        ).place(x=20, y=85)
        # --------------------------------------------------


    # ------------------------------------------------------
    # DATA
    # ------------------------------------------------------
    def refresh_list(self):
        rows = self.controller.get_all_countries()
        self.tree.delete(*self.tree.get_children())
        for idx, r in enumerate(rows):
            tag = "even" if idx % 2 == 0 else "odd"
            self.tree.insert(
                "", "end",
                values=(r["id"], r["name"], r["country_code"], r["population"], r["currency"]),
                tags=(tag,)
            )


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


    # ------------------------------------------------------
    # CRUD
    # ------------------------------------------------------
    def on_add(self):
        self.controller.add_country(
            self.name_var.get(),
            self.code_var.get(),
            self.population_var.get(),
            self.currency_var.get()
        )
        self.refresh_list()
        self.reset_entry()
        
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
        self.reset_entry()

    def reset_entry(self):
        self.name_var.set("")
        self.code_var.set("")
        self.population_var.set("")
        self.currency_var.set("")

    def on_search(self):
        rows = self.controller.search_country(self.search_var.get())
        self.tree.delete(*self.tree.get_children())
        for idx, r in enumerate(rows):
            tag = "even" if idx % 2 == 0 else "odd"
            self.tree.insert(
                "", "end",
                values=(r["id"], r["name"], r["country_code"], r["population"], r["currency"]),
                tags=(tag,)
            )
