import tkinter as tk
from tkinter import ttk, messagebox

class ManageStudyCostWindow(tk.Toplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.title("Manage Study Costs")
        self.geometry("1400x700")
        self.configure(bg="#578FCA")
        self.transient(master)
        self.focus_set()
        header = tk.Label(self, text="Manage Study Costs", bg="#D1F8EF", fg="#3674B5", font=("Arial", 20, "bold"))
        header.pack(side="top", fill="x")

        self.create_widgets()
        self.load_combos()
        self.refresh_list()

    def create_widgets(self):
        mainframe = tk.Frame(self, bg="#578FCA")
        mainframe.pack(fill="both", expand=True, padx=10, pady=10)
        mainframe.grid_columnconfigure(0, weight=8)
        mainframe.grid_columnconfigure(1, weight=2)
        mainframe.grid_rowconfigure(0, weight=1)

        # Left: Treeview
        left_frame = tk.Frame(mainframe, bg="#A1E3F9")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=5,pady=10)
        left_frame.grid_rowconfigure(2, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)
        tk.Label(left_frame, text="Study Cost Records", bg="#A1E3F9", fg="#3674B5", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=5)

        tk.Frame(left_frame, bg="#578FCA", height=10).grid(row=1, column=0, columnspan=2, sticky="ew")

        columns = ("id", "university", "program", "duration", "tuition", "living_idx", "rent", "visa", "insurance", "exchange")
        style = ttk.Style() 
        style.theme_use("clam") 
        style.configure("Treeview.Heading", background="#A1E3F9", foreground="#3674B5", font=("Arial", 8,"bold")) 
        self.tree = ttk.Treeview(left_frame, columns=columns, show="headings", height=20)        
        headers = [
            ("id", "ID", 50), 
            ("university", "University", 200), 
            ("program", "Program", 150),
            ("duration", "Duration(years)", 90), 
            ("tuition", "Tuition(USD/yr)", 90),
            ("living_idx", "Living Index", 90), 
            ("rent", "Rent(USD/mo)", 90),
            ("visa", "Visa(USD)", 90), 
            ("insurance", "Insurance USD", 90), 
            ("exchange", "1USD→VND", 90),
        ]
        for col, text, w in headers:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=w, anchor="center",stretch=False)
        self.tree.grid(row=2, column=0, sticky="nsew")
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        vsb = ttk.Scrollbar(left_frame, orient="vertical", command=self.tree.yview)
        vsb.grid(row=2, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=vsb.set)

        # Right: Form
        right_frame = tk.Frame(mainframe, bg="#A1E3F9")
        right_frame.grid(row=0, column=1,padx=5,pady=10,sticky="nsew")   
        tk.Label(right_frame, text="Cost Details",  bg="#A1E3F9", fg="#3674B5",
        font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=5)
        right_frame.grid_columnconfigure(1, weight=1)
        tk.Frame(right_frame, bg="#578FCA", height=10).grid(row=1, column=0, columnspan=2, sticky="ew")

        row_id = 2  # dùng để tăng row cho grid

        # University & Program
        for label, var, combo in [
            ("University", "uni_var", "uni_combo"),
            ("Program", "prog_var", "prog_combo")
        ]:
            tk.Label(
                right_frame, text=label, bg="#A1E3F9", fg="#3674B5",
                font=("Arial", 10, "bold")
            ).grid(row=row_id, column=0, sticky="e", pady=5)

            setattr(self, var, tk.StringVar())
            cb = ttk.Combobox(
                right_frame, textvariable=getattr(self, var),
                state="readonly", width=25
            )
            setattr(self, combo, cb)
            cb.grid(row=row_id, column=1, sticky="w",padx=10, pady=5)
            row_id += 1


        # Duration
        tk.Label(
            right_frame, text="Duration\n(years)", bg="#A1E3F9", fg="#3674B5",
            font=("Arial", 10, "bold")
        ).grid(row=row_id, column=0, sticky="e", pady=(5, 3))

        self.duration_var = tk.StringVar()
        tk.Entry(right_frame, textvariable=self.duration_var, width=25)\
            .grid(row=row_id, column=1, sticky="w",padx=10, pady=5)
        row_id += 1


        # Cost fields
        self.cost_vars = {}
        fields = [
            ("Tuition\n(USD/year)", "tuition_var"),
            ("Living Cost Index", "living_idx_var"),
            ("Rent\n(USD/month)", "rent_var"),
            ("Visa Fee USD", "visa_var"),
            ("Insurance\n(USD/year) ", "insurance_var"),
            ("Exchange Rate\n(to VND)", "exchange_var"),
        ]

        for label, varname in fields:
            tk.Label(
                right_frame, text=label, bg="#A1E3F9", fg="#3674B5",
                font=("Arial", 10, "bold")
            ).grid(row=row_id, column=0, sticky="e", pady=(5, 3))

            var = tk.StringVar()
            tk.Entry(right_frame, textvariable=var, width=25)\
                .grid(row=row_id, column=1, sticky="w",padx=10, pady=3)

            self.cost_vars[varname] = var
            row_id += 1


        # Search
        tk.Label(
            right_frame, text="Search", bg="#A1E3F9", fg="#3674B5",
            font=("Arial", 10, "bold")
        ).grid(row=row_id, column=0, sticky="e", pady=(5, 3))

        self.search_var = tk.StringVar()
        tk.Entry(right_frame, textvariable=self.search_var, width=25)\
            .grid(row=row_id, column=1, sticky="w",padx=10, pady=5)
        row_id += 1


        # Buttons (Add, Update, Delete, Find, Clear)
        btns = tk.Frame(right_frame, bg="#A1E3F9")
        btns.grid(row=row_id, column=0, columnspan=2, pady=10)

        for i, (text, cmd) in enumerate([
            ("Add", self.on_add),
            ("Update", self.on_update),
            ("Delete", self.on_delete),
            ("Find", self.on_search),
            ("Clear", self.clear_form)
        ]):
            tk.Button(
                btns, text=text, command=cmd,
                bg="#3674B5", fg="white", width=7,
                font=("Arial", 9, "bold")
            ).grid(row=i//3, column=i % 3, padx=8, pady=6)

    def load_combos(self):
        unis = self.controller.get_universities()
        self.uni_combo['values'] = [f"{u['name']} - {u['city']}, {u['country']}" for u in unis]
        self.uni_map = {f"{u['name']} - {u['city']}, {u['country']}": u["id"] for u in unis}

        progs = self.controller.get_programs()
        self.prog_combo['values'] = [f"{p['name']} ({p['level']})" for p in progs]
        self.prog_map = {f"{p['name']} ({p['level']})": p["id"] for p in progs}

    def refresh_list(self):
        rows = self.controller.get_all_study_costs()
        self.tree.delete(*self.tree.get_children())
        for i, r in enumerate(rows):
            tag = "even" if i % 2 == 0 else "odd"
            self.tree.insert("", "end", values=(
                r["id"], r["university"], r["program"],
                r["duration_years"], r["tuition_usd"], r["living_cost_index"],
                r["rent_usd"], r["visa_fee_usd"], r["insurance_usd"], r["exchange_rate"]
            ), tags=(tag,))
        self.tree.tag_configure("even", background="white")
        self.tree.tag_configure("odd", background="#D1F8EF")

    def on_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        cost_id = self.tree.item(sel[0])["values"][0]

        # Lấy 1 lần duy nhất
        row = self.controller.get_cost_by_id(cost_id) 
        if not row:
            return

        # Set combo
        self.uni_var.set(f"{row['university']} - {row['city']}, {row['country']}")
        self.prog_var.set(f"{row['program']} ({row['level']})")

        # Set các field
        fields = {
            "duration_var": row['duration_years'],
            "tuition_var": row['tuition_usd'],
            "living_idx_var": row['living_cost_index'],
            "rent_var": row['rent_usd'],
            "visa_var": row['visa_fee_usd'],
            "insurance_var": row['insurance_usd'],
            "exchange_var": row['exchange_rate'],
        }
        for var_name, value in fields.items():
            getattr(self, var_name, None) and getattr(self, var_name).set(str(value) if value is not None else "")
            if var_name in self.cost_vars:
                self.cost_vars[var_name].set(str(value) if value is not None else "")
    def selected_id(self):
        sel = self.tree.selection()
        return self.tree.item(sel[0])["values"][0] if sel else None

    def get_decimal(self, var):
        val = var.get().strip()
        return float(val) if val else None

    def on_add(self):
        uni_id = self.uni_map.get(self.uni_var.get())
        prog_id = self.prog_map.get(self.prog_var.get())
        if not uni_id or not prog_id:
            messagebox.showwarning("Lỗi", "Vui lòng chọn Trường và Chương trình!")
            return

        try:
            self.controller.add_study_cost(
                university_id=uni_id,
                program_id=prog_id,
                duration_years=self.get_decimal(self.duration_var),
                tuition_usd=self.get_decimal(self.cost_vars["tuition_var"]),
                living_cost_index=self.get_decimal(self.cost_vars["living_idx_var"]),
                rent_usd=self.get_decimal(self.cost_vars["rent_var"]),
                visa_fee_usd=self.get_decimal(self.cost_vars["visa_var"]),
                insurance_usd=self.get_decimal(self.cost_vars["insurance_var"]),
                exchange_rate=self.get_decimal(self.cost_vars["exchange_var"]),
            )
            messagebox.showinfo("Thành công", "Thêm chi phí du học thành công!")
            self.refresh_list()
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thêm:\n{e}")

    def on_update(self):
        cost_id = self.selected_id()
        if not cost_id:
            messagebox.showwarning("Chọn", "Vui lòng chọn một bản ghi!")
            return

        try:
            self.controller.update_study_cost(
                cost_id,
                university_id=self.uni_map.get(self.uni_var.get()),
                program_id=self.prog_map.get(self.prog_var.get()),
                duration_years=self.get_decimal(self.duration_var),
                tuition_usd=self.get_decimal(self.cost_vars["tuition_var"]),
                living_cost_index=self.get_decimal(self.cost_vars["living_idx_var"]),
                rent_usd=self.get_decimal(self.cost_vars["rent_var"]),
                visa_fee_usd=self.get_decimal(self.cost_vars["visa_var"]),
                insurance_usd=self.get_decimal(self.cost_vars["insurance_var"]),
                exchange_rate=self.get_decimal(self.cost_vars["exchange_var"]),
            )
            messagebox.showinfo("Thành công", "Cập nhật thành công!")
            self.refresh_list()
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật:\n{e}")
    def on_delete(self):
        cid = self.selected_id()
        if cid and messagebox.askyesno("Confirm", "Delete this study cost record?"):
            self.controller.delete_study_cost(cid)
            self.refresh_list()
            self.clear_form()

    def on_search(self):
        keyword = self.search_var.get().strip().lower()
        if not keyword:
            self.refresh_list()
            return

        # Lấy toàn bộ dữ liệu
        all_rows = self.controller.get_all_study_costs()

        # Lọc theo [...]
        filtered = []
        for r in all_rows:
            if (
                keyword in str(r.get("university", "")).lower() or
                keyword in str(r.get("program", "")).lower() or
                keyword in str(r.get("duration_years", "")).lower() or
                keyword in str(r.get("tuition_usd", "")).lower() or
                keyword in str(r.get("living_cost_index", "")).lower() or
                keyword in str(r.get("rent_usd", "")).lower() or
                keyword in str(r.get("visa_fee_usd", "")).lower() or
                keyword in str(r.get("insurance_usd", "")).lower() or
                keyword in str(r.get("exchange_rate", "")).lower()
            ):
                filtered.append(r)

        # Xóa và hiển thị kết quả tìm kiếm
        self.tree.delete(*self.tree.get_children())
        
        # Tạo hiệu ứng so le màu
        self.tree.tag_configure("even", background="white")
        self.tree.tag_configure("odd", background="#D1F8EF")

        for i, r in enumerate(filtered):
            tag = "even" if i % 2 == 0 else "odd"
            self.tree.insert("", "end", values=(
                r["id"],
                r["university"],
                r["program"],
                r["duration_years"] or "",
                r["tuition_usd"] or "",
                r["living_cost_index"] or "",
                r["rent_usd"] or "",
                r["visa_fee_usd"] or "",
                r["insurance_usd"] or "",
                r["exchange_rate"] or ""
            ), tags=(tag,))
    def clear_form(self):
        for var in [self.uni_var, self.prog_var, self.duration_var, self.search_var] + list(self.cost_vars.values()):
            var.set("")
        self.tree.selection_remove(self.tree.selection())
        self.refresh_list()