import tkinter as tk
from tkinter import ttk, messagebox

class ManageProgramWindow(tk.Toplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.title("Manage Programs")
        self.geometry("860x600")
        self.configure(bg="#578FCA")
        self.transient(master)
        self.focus_set()
        header = tk.Label(self, text="Manage Programs", bg="#D1F8EF", fg="#3674B5", font=("Arial", 20, "bold"))
        header.pack(side="top", fill="x")

        self.create_widgets()
        self.refresh_list()

    def create_widgets(self):
        # frame chính, đặt nền cùng màu
        mainframe = tk.Frame(self, bg="#578FCA")
        mainframe.pack(fill="both", expand=True, padx=10, pady=10)

        mainframe.grid_columnconfigure(0, weight=7)
        mainframe.grid_columnconfigure(1, weight=3)
        mainframe.grid_rowconfigure(0, weight=1)

        # ===================== LEFT FRAME =====================
        left_frame = tk.Frame(mainframe, bg="#A1E3F9")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=10)
        left_frame.grid_rowconfigure(2, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        # Tiêu đề
        tk.Label(left_frame, text="Program List", bg="#A1E3F9", fg="#3674B5",
                font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=5)

        # Hàng ngăn cách
        tk.Frame(left_frame, bg="#578FCA", height=10).grid(row=1, column=0, columnspan=2, sticky="ew")

        # Treeview
        columns = ("id", "name", "level")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="#A1E3F9", foreground="#3674B5", font=("Arial", 10, "bold"))

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
        right_frame = tk.Frame(mainframe, bg="#A1E3F9")
        right_frame.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")
        right_frame.grid_columnconfigure(1, weight=1)

        tk.Label(right_frame, text="Program Details", bg="#A1E3F9", fg="#3674B5",
                font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=5)

        tk.Frame(right_frame, bg="#578FCA", height=10).grid(row=1, column=0, columnspan=2, sticky="ew")

        # Program Name
        tk.Label(right_frame, text="Program Name", bg="#A1E3F9", fg="#3674B5",
                font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="e", pady=5)
        self.name_var = tk.StringVar()
        tk.Entry(right_frame, textvariable=self.name_var, width=28).grid(row=2, column=1, padx=5, pady=5)

        # Level
        tk.Label(right_frame, text="Level", bg="#A1E3F9", fg="#3674B5",
                font=("Arial", 10, "bold")).grid(row=3, column=0, sticky="e", pady=5)
        self.level_var = tk.StringVar()
        self.level_combo = ttk.Combobox(right_frame, textvariable=self.level_var, width=25)
        self.level_combo.grid(row=3, column=1, padx=5, pady=5)

        # Search
        tk.Label(right_frame, text="Search", bg="#A1E3F9", fg="#3674B5",
                font=("Arial", 10, "bold")).grid(row=4, column=0, sticky="e", pady=5)
        self.search_var = tk.StringVar()
        tk.Entry(right_frame, textvariable=self.search_var, width=28).grid(row=4, column=1, padx=5, pady=5)

        # Buttons
        btns = tk.Frame(right_frame, bg="#A1E3F9")
        btns.grid(row=5, column=0, columnspan=2, padx=20, pady=10)

        tk.Button(btns, text="Add", command=self.on_add, bg="#3674B5", fg="white", width=7).grid(row=0, column=0, pady=2)
        tk.Button(btns, text="Update", command=self.on_update, bg="#3674B5", fg="white", width=7).grid(row=0, column=1, padx=5, pady=2)
        tk.Button(btns, text="Delete", command=self.on_delete, bg="#3674B5", fg="white", width=7).grid(row=0, column=2, padx=5, pady=2)
        tk.Button(btns, text="Find", command=self.on_search, bg="#3674B5", fg="white", width=7).grid(row=1, column=0, padx=5, pady=2)
        tk.Button(btns, text="Clear", command=self.clear_form, bg="#3674B5", fg="white", width=7).grid(row=1, column=1, padx=5, pady=2)

    def refresh_list(self):
        rows = self.controller.get_all_programs()
        self.tree.delete(*self.tree.get_children())

        # Định nghĩa màu so le
        self.tree.tag_configure("even", background="white")
        self.tree.tag_configure("odd", background="#D1F8EF")

        for i, r in enumerate(rows):
            tag = "even" if i % 2 == 0 else "odd"
            self.tree.insert("", "end",
                             values=(r["id"], r["name"], r["level"]),
                             tags=(tag,))

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

    def on_add(self):
        name = self.name_var.get().strip()
        level = self.level_var.get().strip()
        if not name or not level:
            messagebox.showwarning("Thiếu thông tin", "Tên chương trình và cấp độ không được để trống!")
            return
        try:
            self.controller.add_program(name, level)
            messagebox.showinfo("Thành công", f"Đã thêm chương trình:\n{name}")
            self.refresh_list()
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))  # ví dụ lỗi UNIQUE constraint

    def on_update(self):
        pid = self.selected_id()
        if not pid:
            messagebox.showwarning("Chọn", "Vui lòng chọn một chương trình để cập nhật!")
            return
        name = self.name_var.get().strip()
        level = self.level_var.get().strip()
        if not name or not level:
            messagebox.showwarning("Thiếu thông tin", "Tên chương trình và cấp độ không được để trống!")
            return
        self.controller.update_program(pid, name, level)
        self.refresh_list()
        self.clear_form()
        messagebox.showinfo("Thành công", "Chương trình đã được cập nhật!")

    def on_delete(self):
        pid = self.selected_id()
        if not pid:
            messagebox.showwarning("Chọn", "Vui lòng chọn một chương trình để xóa!")
            return
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa chương trình này?\nCác chi phí học tập liên quan cũng sẽ bị xóa!"):
            self.controller.delete_program(pid)
            self.refresh_list()
            self.clear_form()
            messagebox.showinfo("Thành công", "Chương trình đã được xóa!")

    def on_search(self):
        keyword = self.search_var.get().strip().lower()
        if not keyword:
            self.refresh_list()
            return

        all_programs = self.controller.get_all_programs()
        filtered = []
        for r in all_programs:
            if (keyword in r["name"].lower() or 
                keyword in r["level"].lower()):  # Tìm thêm trong level
                filtered.append(r)

        self.tree.delete(*self.tree.get_children())
        for i, r in enumerate(filtered):
            tag = "even" if i % 2 == 0 else "odd"
            self.tree.insert("", "end", values=(r["id"], r["name"], r["level"]), tags=(tag,))
    def clear_form(self):
        self.name_var.set("")
        self.level_var.set("")
        self.search_var.set("")
        self.tree.selection_remove(self.tree.selection())
        self.tree.focus("")
        self.refresh_list()
