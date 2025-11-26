import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
from resource_utils import resource_path   # 🔥 dùng helper chung

class ManageProgramWindow(tk.Toplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.title("Manage Programs")
        self.geometry("850x600")
        self.configure(bg="white")
        self.focus_set()

        header = tk.Label(
            self,
            text="📑Manage Programs",
            bg="#1E88E5",
            fg="white",
            font=("Segoe", 16, "bold")
        )
        header.pack(side="top", fill="x", padx=5)

        self.load_icons()  # gọi trước create_widgets()
        self.setup_styles()
        self.create_widgets()
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
        # frame chính, đặt nền cùng màu
        mainframe = tk.Frame(self, bg="white")
        mainframe.pack(fill="both", expand=True, padx=10)

        mainframe.grid_columnconfigure(0, weight=7)
        mainframe.grid_columnconfigure(1, weight=3)
        mainframe.grid_rowconfigure(0, weight=1)

        # ===================== LEFT FRAME =====================
        left_frame = tk.Frame(mainframe, bg="#1E88E5", bd=1, relief="solid")
        left_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=5, pady=10)
        left_frame.grid_rowconfigure(2, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        # Tiêu đề
        tk.Label(
            left_frame,
            text="📑 Program List",
            bg="#1E88E5",
            fg="white",
            font=("Segoe UI", 12, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=5)

        # Hàng ngăn cách
        tk.Frame(left_frame, bg="white", height=3).grid(
            row=1, column=0, columnspan=2, sticky="ew"
        )

        # Treeview
        columns = ("id", "name", "level")
        self.tree = ttk.Treeview(left_frame, columns=columns, show="headings", height=20)
        headers = [
            ("id", "ID", 100),
            ("name", "Program Name", 250),
            ("level", "Level", 150),
        ]
        for col, text, width in headers:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor="center", stretch=False)

        self.tree.grid(row=2, column=0, sticky="nsew")
        scroll = ttk.Scrollbar(left_frame, orient="vertical", command=self.tree.yview)
        scroll.grid(row=2, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # ===================== RIGHT FRAME =====================
        right_frame = tk.Frame(mainframe, bg="white", bd=1, relief="solid")
        right_frame.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")
        right_frame.grid_columnconfigure(1, weight=1)

        heading = tk.Frame(right_frame, bg="#1E88E5")
        heading.grid(row=0, column=0, columnspan=2, sticky="ew")
        tk.Label(
            heading,
            text="✏️ Program Details",
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

        # Program Name
        tk.Label(
            right_frame,
            text="Program Name",
            bg="white",
            fg="#3674B5",
            font=("Arial", 10, "bold")
        ).grid(row=3, column=0, padx=(10, 0), sticky="e", pady=5)
        self.name_var = tk.StringVar()
        tk.Entry(right_frame, textvariable=self.name_var, width=28).grid(
            row=3, column=1, padx=(5, 10), pady=5
        )

        # Level
        tk.Label(
            right_frame,
            text="Level",
            bg="white",
            fg="#3674B5",
            font=("Arial", 10, "bold")
        ).grid(row=4, column=0, padx=(10, 0), sticky="e", pady=5)
        self.level_var = tk.StringVar()
        self.levels = ["Bachelor", "Master", "PhD"]
        self.level_combo = ttk.Combobox(right_frame, textvariable=self.level_var,values=self.levels, state="normal", width=25)
        self.level_combo.grid(row=4, column=1, padx=(5, 10), pady=5)

        # Buttons
        btns = tk.Frame(right_frame, bg="white")
        btns.grid(row=5, column=0, columnspan=2, pady=10)

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
        ).grid(row=0, column=1, padx=5, pady=2)
        tk.Button(
            btns,
            text="Delete",
            command=self.on_delete,
            image=self.delete_icon,
            compound="left",
            width=60,
            **self.btn_normal
        ).grid(row=0, column=2, padx=5, pady=2)
        tk.Button(
            btns,
            text="Clear",
            command=self.clear_form,
            image=self.clear_icon,
            compound="left",
            **self.btn_normal
        ).grid(row=0, column=3, padx=5, pady=2)

        # ---- Summary Card: Total Programs ----
        card_frame = tk.Frame(mainframe, bg="white", bd=1, relief="solid")
        card_frame.grid(row=1, column=1, pady=5, sticky="n")

        summary_card = tk.Frame(card_frame, width=280, height=140, bd=0, relief="flat")
        summary_card.pack()
        summary_card.pack_propagate(False)

        # Background image hoặc màu nền
        try:
            bg_img = Image.open(resource_path("views/images/program.png")).resize((280, 140))
            self.program_card_bg = ImageTk.PhotoImage(bg_img)
            tk.Label(summary_card, image=self.program_card_bg, bd=0).place(x=0, y=0)
        except Exception:
            summary_card.configure(bg="#FFE0B2")  # màu nền dự phòng
            tk.Label(summary_card, bg="#FFE0B2").place(x=0, y=0, relwidth=1, relheight=1)

        # Lấy tổng số Programs
        try:
            total_programs = len(self.controller.get_all_programs())
        except Exception:
            total_programs = 0

        # Số lượng hiển thị lớn
        self.program_count_label = tk.Label(
            summary_card,
            text=str(total_programs),
            font=("Segoe UI", 32, "bold"),
            fg="#3674B5",
            bg=summary_card["bg"]
        )
        self.program_count_label.place(x=20, y=30)

        # Text mô tả
        tk.Label(
            summary_card,
            text="Total Programs",
            font=("Segoe UI", 12, "bold"),
            fg="#3674B5",
            bg=summary_card["bg"]
        ).place(x=20, y=85)

    # ------------------------------------------------------
    # DATA
    # ------------------------------------------------------
    def refresh_list(self):
        rows = self.controller.get_all_programs()
        self.tree.delete(*self.tree.get_children())

        # Định nghĩa màu so le
        self.tree.tag_configure("even", background="white")
        self.tree.tag_configure("odd", background="#D1F8EF")

        for i, r in enumerate(rows):
            tag = "even" if i % 2 == 0 else "odd"
            self.tree.insert(
                "",
                "end",
                values=(r["id"], r["name"], r["level"]),
                tags=(tag,)
            )

    def on_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        values = self.tree.item(sel[0])["values"]
        _id, name, level = values
        self.name_var.set(name)
        self.level_var.set(level)

    def selected_id(self):
        sel = self.tree.selection()
        if not sel:
            return None
        return self.tree.item(sel[0])["values"][0]

    # ------------------------------------------------------
    # CRUD
    # ------------------------------------------------------
    def on_add(self):
        name = self.name_var.get().strip()
        level = self.level_var.get().strip()

        if not name or not level:
            messagebox.showwarning("Thiếu thông tin", "Tên chương trình và Level là bắt buộc!", parent=self)
            return

        try:
            self.controller.add_program(name, level)

            # Nếu level mới, thêm vào combobox
            if level not in self.levels:
                self.levels.append(level)
                self.level_combo['values'] = self.levels

            self.refresh_list()
            self.update_total_count()
            self.clear_form()
            self.focus_set()
            messagebox.showinfo("Thành công", f"Đã thêm chương trình:\n{name}", parent=self)
        except Exception as e:
            messagebox.showerror("Lỗi", str(e), parent=self)


    def on_update(self):
        pid = self.selected_id()
        if not pid:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một chương trình để cập nhật!", parent=self)
            return

        new_name = self.name_var.get().strip()
        new_level = self.level_var.get().strip()

        if not new_name or not new_level:
            messagebox.showwarning("Lỗi nhập liệu", "Tên chương trình/Level là bắt buộc!", parent=self)
            return

        old_item = self.controller.model.get_program_by_id(pid)

        if not old_item:
            messagebox.showerror("Lỗi", "Không tìm thấy chương trình!", parent=self)
            return

        old_name = old_item["name"]
        old_level = old_item["level"]

        if new_name == old_name and new_level == old_level:
            messagebox.showinfo("Không thay đổi", "Không có thay đổi nào để cập nhật.", parent=self)
            return

        self.controller.update_program(pid, new_name, new_level)
        self.refresh_list()
        self.clear_form()
        self.update_total_count()

        messagebox.showinfo("Thành công", "Cập nhật chương trình thành công!", parent=self)
        self.focus_set()


    def on_delete(self):
        pid = self.selected_id()
        if not pid:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một chương trình để xóa!", parent=self)
            return

        if messagebox.askyesno(
            "Xác nhận xóa",
            "Bạn có chắc chắn muốn xóa chương trình này?\nCác chi phí học liên quan cũng sẽ bị xóa!",
            parent=self
        ):
            self.controller.delete_program(pid)
            self.refresh_list()
            self.clear_form()
            self.update_total_count()   
            messagebox.showinfo("Thành công", "Xóa chương trình thành công!", parent=self)
            self.focus_set()

    def on_search(self):
        keyword = self.search_var.get().strip()
        if not keyword:
            self.refresh_list()
            return

        filtered = self.controller.search_program(keyword=keyword)

        self.tree.delete(*self.tree.get_children())
        for i, r in enumerate(filtered):
            tag = "even" if i % 2 == 0 else "odd"
            self.tree.insert(
                "",
                "end",
                values=(r["id"], r["name"], r["level"]),
                tags=(tag,)
            )

    def update_total_count(self):
        try:
            total = len(self.controller.get_all_programs())
            self.program_count_label.config(text=str(total))
        except Exception:
            self.program_count_label.config(text="0")

    def clear_form(self):
        self.name_var.set("")
        self.level_var.set("")
        self.search_var.set("")
        self.tree.selection_remove(self.tree.selection())
        self.tree.focus("")
        self.refresh_list()
