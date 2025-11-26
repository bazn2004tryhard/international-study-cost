import tkinter as tk
from PIL import Image, ImageTk
from mysql.connector.errors import IntegrityError
from tkinter import ttk, messagebox
from resource_utils import resource_path   # 🔥 dùng helper chung

class ManageUniversityWindow(tk.Toplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.title("Manage University")
        self.geometry("990x600")
        self.resizable(False, False) #khong cho keo full man hinh
        self.focus_set()
        self.configure(bg="white")

        header = tk.Label(
            self,
            text="🏫 Manage University",
            bg="#1E88E5",
            fg="white",
            font=("Segoe", 16, "bold")
        )
        header.pack(side="top", fill="x", padx=5)

        self.load_icons()  # gọi trước create_widgets()
        self.setup_styles()
        self.create_widgets()
        self.load_countries()
        self.refresh_list()

    # ------------------------------------------------------
    # LOAD ICONS (ĐÃ SỬA DÙNG resource_path)
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
        self.clear_icon = ImageTk.PhotoImage(
            Image.open(resource_path("views/icons/clear.png")).resize((18, 18))
        )

    # ------------------------------------------------------
    # STYLES
    # ------------------------------------------------------
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
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
            background="#1E88E5"
        )
        style.map("Treeview", background=[("selected", "#5D866C")])

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
        # frame chính
        mainframe = tk.Frame(self, bg="white")
        mainframe.pack(fill="both", expand=True, padx=10)

        mainframe.grid_columnconfigure(0, weight=8)
        mainframe.grid_columnconfigure(1, weight=2)
        mainframe.grid_rowconfigure(0, weight=1)

        # LEFT FRAME
        left_frame = tk.Frame(mainframe, bg="#1E88E5", bd=1, relief="solid")
        left_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=5, pady=10)
        left_frame.grid_rowconfigure(2, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        tk.Label(
            left_frame,
            text="🏫 University List",
            bg="#1E88E5",
            fg="white",
            font=("Segoe UI", 12, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=5)

        tk.Frame(left_frame, bg="white", height=3).grid(
            row=1, column=0, columnspan=2, sticky="ew"
        )

        columns = ("id", "name", "city", "country", "address")
        self.tree = ttk.Treeview(left_frame, columns=columns, show="headings", height=20)
        headers = [
            ("id", "ID", 70),
            ("name", "University Name", 250),
            ("city", "City", 120),
            ("country", "Country", 100),
            ("address", "Address", 120),
        ]
        for col, text, width in headers:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor="center", stretch=False)

        self.tree.grid(row=2, column=0, sticky="nsew")
        scroll = ttk.Scrollbar(left_frame, orient="vertical", command=self.tree.yview)
        scroll.grid(row=2, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # RIGHT FRAME (form)
        right_frame = tk.Frame(mainframe, bg="white", bd=1, relief="solid")
        right_frame.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")
        right_frame.grid_columnconfigure(1, weight=1)

        heading = tk.Frame(right_frame, bg="#1E88E5")
        heading.grid(row=0, column=0, columnspan=2, sticky="ew")
        tk.Label(
            heading,
            text="✏️ University Details",
            bg="#1E88E5",
            fg="white",
            font=("Segoe UI", 12, "bold")
        ).pack(pady=5, fill="x")

        tk.Frame(right_frame, bg="white", height=3).grid(
            row=1, column=0, columnspan=2, sticky="ew"
        )

        # Search
        search_frame = tk.Frame(right_frame, bg="white")
        search_frame.grid(row=2, column=0, columnspan=2, pady=10)
        tk.Label(
            search_frame,
            text="Search",
            bg="white",
            fg="#3674B5",
            font=("Arial", 10, "bold")
        ).grid(row=0, column=0, sticky="w", pady=5)

        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var, width=25).grid(
            row=0, column=1, pady=5
        )
        tk.Button(
            search_frame,
            text="Find",
            command=self.on_search,
            image=self.find_icon,
            compound="left",
            width=60,
            **self.btn_normal
        ).grid(row=0, column=2, padx=5, pady=2)

        # Country
        tk.Label(
            right_frame,
            text="Country",
            bg="white",
            fg="#3674B5",
            font=("Arial", 10, "bold")
        ).grid(row=3, column=0, padx=(10, 0), sticky="w", pady=5)
        self.country_var = tk.StringVar()
        self.country_combo = ttk.Combobox(
            right_frame,
            textvariable=self.country_var,
            state="readonly",
            width=27
        )
        self.country_combo.grid(row=3, column=1, padx=(5, 10), pady=5)
        self.country_combo.bind("<<ComboboxSelected>>", self.on_country_changed)

        # City
        tk.Label(
            right_frame,
            text="City",
            bg="white",
            fg="#3674B5",
            font=("Arial", 10, "bold")
        ).grid(row=4, column=0, padx=(10, 0), sticky="w", pady=5)
        self.city_var = tk.StringVar()
        self.city_combo = ttk.Combobox(
            right_frame,
            textvariable=self.city_var,
            state="readonly",
            width=27
        )
        self.city_combo.grid(row=4, column=1, padx=(5, 10), pady=5)

        # University name
        tk.Label(
            right_frame,
            text="University",
            bg="white",
            fg="#3674B5",
            font=("Arial", 10, "bold")
        ).grid(row=5, column=0, padx=(10, 0), sticky="w", pady=5)
        self.name_var = tk.StringVar()
        tk.Entry(right_frame, textvariable=self.name_var, width=30).grid(
            row=5, column=1, padx=(5, 10), pady=5
        )

        # Address
        tk.Label(
            right_frame,
            text="Address",
            bg="white",
            fg="#3674B5",
            font=("Arial", 10, "bold")
        ).grid(row=6, column=0, padx=(10, 0), sticky="w", pady=5)
        self.addr_var = tk.StringVar()
        tk.Entry(right_frame, textvariable=self.addr_var, width=30).grid(
            row=6, column=1, padx=(5, 10), pady=5
        )

        # Buttons
        btns = tk.Frame(right_frame, bg="white")
        btns.grid(row=7, column=0, columnspan=2, pady=10)

        tk.Button(
            btns,
            text="Add",
            command=self.on_add,
            image=self.add_icon,
            compound="left",
            width=60,
            **self.btn_normal
        ).grid(row=0, column=0, pady=2)

        tk.Button(
            btns,
            text="Update",
            command=self.on_update,
            image=self.update_icon,
            compound="left",
            width=60,
            **self.btn_normal
        ).grid(row=0, column=1, padx=3, pady=2)

        tk.Button(
            btns,
            text="Delete",
            command=self.on_delete,
            image=self.delete_icon,
            compound="left",
            width=60,
            **self.btn_normal
        ).grid(row=0, column=2, pady=2)

        tk.Button(
            btns,
            text="Clear",
            command=self.clear_form,
            width=60,
            image=self.clear_icon,
            compound="left",
            **self.btn_normal
        ).grid(row=0, column=3, padx=3, pady=2)

        # ---- Summary Card: Total Universities ----
        card_frame = tk.Frame(mainframe, bg="white", bd=1, relief="solid")
        card_frame.grid(row=1, column=1, pady=5, sticky="n")

        summary_card = tk.Frame(card_frame, width=280, height=140, bd=0, relief="flat")
        summary_card.pack()
        summary_card.pack_propagate(False)

        # Background image hoặc màu nền (ĐÃ SỬA DÙNG resource_path)
        try:
            bg_img = Image.open(
                resource_path("views/images/university.png")
            ).resize((280, 140))
            self.uni_card_bg = ImageTk.PhotoImage(bg_img)
            tk.Label(summary_card, image=self.uni_card_bg, bd=0).place(x=0, y=0)
        except Exception:
            summary_card.configure(bg="#3674B5")
            tk.Label(summary_card, bg="#3674B5").place(
                x=0, y=0, relwidth=1, relheight=1
            )

        # Lấy tổng số University
        try:
            total_universities = len(self.controller.get_all_universities())
        except Exception:
            total_universities = 0

        self.uni_count_label = tk.Label(
            summary_card,
            text=str(total_universities),
            font=("Segoe UI", 32, "bold"),
            fg="#3674B5",
            bg=summary_card["bg"]
        )
        self.uni_count_label.place(x=20, y=30)

        tk.Label(
            summary_card,
            text="Total Universities",
            font=("Segoe UI", 12, "bold"),
            fg="#3674B5",
            bg=summary_card["bg"]
        ).place(x=20, y=85)

    # ------------------------------------------------------
    # DATA HELPERS
    # ------------------------------------------------------
    def load_countries(self):
        countries = self.controller.get_countries()
        values = [c["name"] for c in countries]
        self.country_combo.configure(values=values)
        self.country_map = {c["name"]: c["id"] for c in countries}

    def load_cities(self, country_id):
        cities = self.controller.get_cities_by_country(country_id)
        values = [ci["name"] for ci in cities]
        self.city_combo.configure(values=values)
        self.city_map = {ci["name"]: ci["id"] for ci in cities}

    def refresh_list(self):
        rows = self.controller.get_all_universities()
        self.tree.delete(*self.tree.get_children())

        self.tree.tag_configure("evenrow", background="white")
        self.tree.tag_configure("oddrow", background="#D1F8EF")

        for i, r in enumerate(rows):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree.insert(
                "",
                "end",
                values=(
                    r["id"],
                    r["name"],
                    r["city"],
                    r["country"],
                    r.get("address", ""),
                ),
                tags=(tag,),
            )

    # ===================== SELECT ROW =====================
    def on_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        item = self.tree.item(sel[0])
        _id, name, city, country, address = item["values"]

        self.name_var.set(name)
        self.addr_var.set(address)
        self.country_var.set(country)

        country_id = self.country_map.get(country)
        if country_id:
            self.load_cities(country_id)
            if city in [c["name"] for c in self.controller.get_cities_by_country(country_id)]:
                self.city_var.set(city)
            else:
                self.city_var.set("")
        else:
            self.city_combo.configure(values=[])
            self.city_var.set("")

    def selected_id(self):
        sel = self.tree.selection()
        if not sel:
            return None
        return self.tree.item(sel[0])["values"][0]

    # ===================== CRUD =====================
    def on_add(self):
        name = self.name_var.get().strip()
        city_name = self.city_var.get().strip()

        if not name:
            messagebox.showwarning("Thiếu thông tin", "Tên trường đại học không được để trống!")
            return
        if not city_name:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn thành phố!")
            return

        city_id = self.city_map.get(city_name)
        if not city_id:
            messagebox.showerror("Lỗi", "Thành phố không hợp lệ!")
            return

        address = self.addr_var.get().strip() or None

        try:
            self.controller.add_university(name, city_id, address)
            self.refresh_list()
            self.update_total_count()
            self.clear_form()
            self.focus_set()
            messagebox.showinfo("Thành công", f"Đã thêm trường:\n{name}", parent=self)
        except IntegrityError as e:
            if e.errno == 1062:
                messagebox.showerror(
                    "Đã tồn tại",
                    f"Trường '{name}' đã có trong thành phố '{city_name}'!\nKhông thể thêm trùng.",
                    parent=self
                )
            else:
                messagebox.showerror("Lỗi CSDL", str(e), parent=self)
        except Exception as e:
            messagebox.showerror("Lỗi không xác định", str(e), parent=self)

    def on_update(self):
        uid = self.selected_id()
        if not uid:
            messagebox.showwarning(
                "Warning", "Vui lòng chọn một trường đại học để cập nhật!", parent=self
            )
            return

        new_name = self.name_var.get().strip()
        new_city_name = self.city_var.get().strip()
        new_addr = self.addr_var.get().strip() or None

        if not new_name:
            messagebox.showwarning("Input Error", "University name is required!", parent=self)
            return
        if not new_city_name:
            messagebox.showwarning("Input Error", "Please select a city!", parent=self)
            return

        new_city_id = self.city_map.get(new_city_name)
        if not new_city_id:
            messagebox.showerror("Error", "Invalid city selected!", parent=self)
            return

        old_item = self.controller.get_university(uid)
        old_name = old_item["name"]
        old_city_id = old_item["city_id"]
        old_addr = old_item["address"]

        if (
            new_name == old_name
            and new_city_id == old_city_id
            and (new_addr or "") == (old_addr or "")
        ):
            messagebox.showinfo("No Change", "No changes detected to update.", parent=self)
            return

        try:
            self.controller.update_university(uid, new_name, new_city_id, new_addr)
            self.refresh_list()
            self.update_total_count()
            self.clear_form()
            self.focus_set()
            messagebox.showinfo("Success", "University updated successfully!", parent=self)
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e), parent=self)
        except Exception as e:
            messagebox.showerror("Lỗi không xác định", str(e), parent=self)

    def on_delete(self):
        uid = self.selected_id()
        if not uid:
            messagebox.showwarning(
                "Warning", "Please select a university to delete!"
            )
            return
        if messagebox.askyesno(
            "Confirm Delete", "Are you sure you want to delete this university?", parent=self
        ):
            try:
                self.controller.delete_university(uid)
                self.refresh_list()
                self.update_total_count()
                self.clear_form()
                self.focus_set()
                messagebox.showinfo("Success", "University deleted!", parent=self)
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa: {str(e)}", parent=self)

    def on_search(self):
        keyword = self.search_var.get().strip() if self.search_var.get() else ""

        if not keyword:
            self.refresh_list()
            return
        
        keyword = keyword.lower()

        all_rows = self.controller.get_all_universities()
        filtered = []
        for r in all_rows:
            if (
                keyword in r["name"].lower()
                or keyword in r["city"].lower()
                or keyword in r["country"].lower()
                or (r.get("address") and keyword in r["address"].lower())
            ):
                filtered.append(r)

        self.tree.delete(*self.tree.get_children())
        self.tree.tag_configure("evenrow", background="white")
        self.tree.tag_configure("oddrow", background="#D1F8EF")

        for i, r in enumerate(filtered):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree.insert(
                "",
                "end",
                values=(
                    r["id"],
                    r["name"],
                    r["city"],
                    r["country"],
                    r.get("address", ""),
                ),
                tags=(tag,),
            )

    def on_country_changed(self, choice=None):
        country_name = self.country_var.get().strip()
        if not country_name:
            self.city_combo.configure(values=[])
            self.city_var.set("")
            self.city_map = {}
            return

        country_id = self.country_map.get(country_name)
        if country_id:
            self.load_cities(country_id)
            self.city_var.set("")
        else:
            self.city_combo.configure(values=[])
            self.city_var.set("")
            self.city_map = {}

    def clear_form(self):
        self.name_var.set("")
        self.addr_var.set("")
        self.country_var.set("")
        self.city_var.set("")
        self.search_var.set("")
        self.city_combo.configure(values=[])
        self.tree.selection_remove(self.tree.selection())
        self.tree.focus("")
        self.refresh_list()
    
    def update_total_count(self):
        """Update the total count label"""
        try:
            total = len(self.controller.get_all_universities())
            self.uni_count_label.config(text=str(total))
        except Exception:
            self.uni_count_label.config(text="0")
