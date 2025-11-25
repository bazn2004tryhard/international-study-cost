import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
from resource_utils import resource_path   # 🔥 dùng file helper chung

class ManageCityWindow(tk.Toplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.title("Manage City")
        self.geometry("980x540")
        self.configure(bg="white")

        self.load_icons()
        self.setup_styles()

        self.create_widgets()
        self.refresh_list()

    # ------------------------------------------------------
    # LOAD ICONS  (ĐÃ SỬA DÙNG resource_path)
    # ------------------------------------------------------
    def load_icons(self):
        self.add_icon = ImageTk.PhotoImage(
            Image.open(resource_path("views/icons/add.png")).resize((18, 18))
        )
        self.update_icon = ImageTk.PhotoImage(
            Image.open(resource_path("views/icons/update.png")).resize((18, 18))
        )
        self.delete_icon = ImageTk.PhotoImage(
            Image.open(resource_path("views/icons/delete.png")).resize((18, 18))
        )
        self.find_icon = ImageTk.PhotoImage(
            Image.open(resource_path("views/icons/find.png")).resize((18, 18))
        )
        self.country_icon = ImageTk.PhotoImage(
            Image.open(resource_path("views/icons/country.png")).resize((18, 18))
        )

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
            background="#3674B5"
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
            text="🌍 City List",
            bg="#1E88E5",
            fg="white",
            font=("Segoe UI", 12, "bold"),
            pady=8
        )
        title_label.pack(fill="x")

        table_frame = tk.Frame(table_card, bg="white")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("id", "city", "country_id", "city_code")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=18)

        headers = [
            ("id", "ID"),
            ("city", "City Name"),
            ("country_id", "Country Id"),
            ("city_code", "City Code")
        ]

        for col, text in headers:
            self.tree.heading(col, text=text)
            width = 200 if col == "city" else (60 if col == "id" else 120)
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
            text="✏️ City Form",
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
        self.city_var = tk.StringVar()
        self.country_id_var = tk.StringVar()
        self.city_code_var = tk.StringVar()

        fields = [
            ("City:", self.city_var),
            ("Country Id:", self.country_id_var),
            ("City Code:", self.city_code_var)
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
        # CARD TỔNG SỐ City (row=1, col=1)
        # --------------------------------------------------
        card_frame = tk.Frame(main_frame, bg="white")
        card_frame.grid(row=1, column=1, sticky="n", pady=(10, 0))

        summary_card = tk.Frame(card_frame, width=300, height=150, bd=0, relief="flat", bg=None)
        summary_card.pack()

        # ---- Background image ----
        try:
            bg_img = Image.open(resource_path("views/images/city.jpg")).resize((300, 150))
            self.card_bg = ImageTk.PhotoImage(bg_img)
            tk.Label(summary_card, image=self.card_bg, bd=0).place(x=0, y=0)
        except Exception:
            summary_card.configure(bg="#1E88E5")
            tk.Label(summary_card, bg="#1E88E5").place(x=0, y=0, relwidth=1, relheight=1)

        # ---- Total cities ----
        try:
            total = len(self.controller.get_all_cities())
        except Exception:
            total = 0

        tk.Label(
            summary_card,
            text=str(total),
            font=("Segoe UI", 36, "bold"),
            fg="white",
            bg="#7C7E7C"
        ).place(x=20, y=30)

        tk.Label(
            summary_card,
            text="Total Cities",
            font=("Segoe UI", 12),
            fg="white",
            bg="#7C7E7C",
        ).place(x=20, y=85)

    # ------------------------------------------------------
    # DATA
    # ------------------------------------------------------
    def refresh_list(self):
        rows = self.controller.get_all_cities()
        self.tree.delete(*self.tree.get_children())
        for idx, r in enumerate(rows):
            tag = "even" if idx % 2 == 0 else "odd"
            self.tree.insert(
                "", "end",
                values=(r["id"], r["city"], r["country_id"], r["city_code"]),
                tags=(tag,)
            )

    def on_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        item = self.tree.item(sel[0])
        _id, city, country_id, city_code = item["values"]

        self.city_var.set(city)
        self.country_id_var.set(country_id)
        self.city_code_var.set(city_code)

    def selected_id(self):
        sel = self.tree.selection()
        if not sel:
            return None
        return self.tree.item(sel[0])["values"][0]

    # ------------------------------------------------------
    # CRUD
    # ------------------------------------------------------
    def on_add(self):
        if not self.check_entry():
            return
        self.controller.add_city(
            self.city_var.get(),
            self.country_id_var.get(),
            self.city_code_var.get()
        )
        self.refresh_list()
        self.reset_entry()
        messagebox.showinfo("Success", "City added successfully!")

    def on_update(self):
        if not self.check_entry():
            return
        cid = self.selected_id()
        if not cid:
            return messagebox.showwarning("Warning", "Select an item first")
        self.controller.update_city(
            cid,
            self.city_var.get(),
            self.country_id_var.get(),
            self.city_code_var.get()
        )
        self.refresh_list()
        messagebox.showinfo("Success", "City updated successfully!")

    def on_delete(self):
        cid = self.selected_id()
        if not cid:
            return messagebox.showwarning("Warning", "Select an item first")
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this city?"):
            success = self.controller.delete_city(cid)
            if success:
                messagebox.showinfo("Success", "City deleted successfully")
                self.refresh_list()
                self.reset_entry()
            else:
                messagebox.showerror("Error", "Failed to delete city")

    def reset_entry(self):
        self.city_var.set("")
        self.country_id_var.set("")
        self.city_code_var.set("")

    def on_search(self):
        rows = self.controller.search_city(self.search_var.get())
        self.tree.delete(*self.tree.get_children())
        for idx, r in enumerate(rows):
            tag = "even" if idx % 2 == 0 else "odd"
            self.tree.insert(
                "", "end",
                values=(r["id"], r["city"], r["country_id"], r["city_code"]),
                tags=(tag,)
            )

    # ------------------------------------------------------
    # VALIDATE
    # ------------------------------------------------------
    def check_entry(self):
        if not self.city_var.get().strip() or not self.country_id_var.get().strip() or not self.city_code_var.get().strip():
            messagebox.showwarning("Warning", "All fields are required")
            return False

        if not self.country_id_var.get().isdigit():
            messagebox.showwarning("Warning", "Country ID must be a number")
            return False

        if not self.city_code_var.get().isdigit():
            messagebox.showwarning("Warning", "City Code must be a number")
            return False

        return True
