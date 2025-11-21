import tkinter as tk
from mysql.connector.errors import IntegrityError
from tkinter import ttk, messagebox

class ManageUniversityWindow(tk.Toplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.title("Manage University")
        self.geometry("990x600")
        self.transient(master)
        self.focus_set()
        # đặt màu nền cho toàn bộ cửa sổ
        self.configure(bg="#578FCA")

        # thêm label tiêu đề
        header = tk.Label(self, text="Manage University",
                          bg="#D1F8EF", fg="#3674B5",
                          font=("Arial", 20, "bold"))
        header.pack(side="top",fill="x", pady=0)

        self.create_widgets()
        self.load_countries()
        self.refresh_list()

    def create_widgets(self):
    # frame chính, đặt nền cùng màu
        mainframe = tk.Frame(self, bg="#578FCA")
        mainframe.pack(fill="both", expand=True, padx=10, pady=10)

        mainframe.grid_columnconfigure(0, weight=8)
        mainframe.grid_columnconfigure(1, weight=2)
        mainframe.grid_rowconfigure(0, weight=1)

        left_frame = tk.Frame(mainframe, bg="#A1E3F9")
        left_frame.grid(row=0, column=0, sticky="nsew",padx=5,pady=10)
        left_frame.grid_rowconfigure(2, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)
        # Left frame title
        tk.Label(left_frame, text="University List", bg="#A1E3F9", fg="#3674B5",
                font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=5)

        # Hàng trắng ngăn cách
        tk.Frame(left_frame, bg="#578FCA", height=10).grid(row=1, column=0, columnspan=2, sticky="ew")

        # Treeview
        columns = ("id", "name", "city", "country", "address")
        style = ttk.Style() 
        style.theme_use("clam") 
        style.configure("Treeview.Heading", background="#A1E3F9", foreground="#3674B5", font=("Arial", 10,"bold")) 
        self.tree = ttk.Treeview(left_frame, columns=columns, show="headings", height=20)
        headers = [
            ("id", "ID", 70),
            ("name", "University Name", 200),
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



        # ===================== FORM =====================
        right_frame = tk.Frame(mainframe, bg="#A1E3F9")
        right_frame.grid(row=0, column=1,padx=5,pady=10,sticky="nsew")   
        tk.Label(right_frame, text="University Details",  bg="#A1E3F9", fg="#3674B5",
        font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=5)
        right_frame.grid_columnconfigure(1, weight=1)
        tk.Frame(right_frame, bg="#578FCA", height=10).grid(row=1, column=0, columnspan=2, sticky="ew")

        # Country
        tk.Label(right_frame, text="Country", bg="#A1E3F9", fg="#3674B5",font=("Arial", 10,"bold")).grid(row=2, column=0, sticky="e",pady=5)
        self.country_var = tk.StringVar()
        self.country_combo = ttk.Combobox(right_frame, textvariable=self.country_var, state="readonly", width=25)
        self.country_combo.grid(row=2, column=1, padx=5,pady=5)
        self.country_combo.bind("<<ComboboxSelected>>", self.on_country_changed)

        # City
        tk.Label(right_frame, text="City", bg="#A1E3F9", fg="#3674B5",font=("Arial", 10,"bold")).grid(row=3, column=0, sticky="e",pady=5)
        self.city_var = tk.StringVar()
        self.city_combo = ttk.Combobox(right_frame, textvariable=self.city_var, state="readonly", width=25)
        self.city_combo.grid(row=3, column=1, padx=5,pady=5)

        # University name
        tk.Label(right_frame, text="University Name", bg="#A1E3F9", fg="#3674B5",font=("Arial", 10,"bold")).grid(row=4, column=0, sticky="e",pady=5)
        self.name_var = tk.StringVar()
        tk.Entry(right_frame, textvariable=self.name_var, width=28).grid(row=4, column=1, padx=5,pady=5)

        # Address
        tk.Label(right_frame, text="Address", bg="#A1E3F9", fg="#3674B5",font=("Arial", 10,"bold")).grid(row=5, column=0, sticky="e",pady=5)
        self.addr_var = tk.StringVar()
        tk.Entry(right_frame, textvariable=self.addr_var, width=28).grid(row=5, column=1, padx=5,pady=5)
        
        # Search
        tk.Label(right_frame, text="Search", bg="#A1E3F9", fg="#3674B5",font=("Arial", 10,"bold")).grid(row=6, column=0, sticky="e",pady=5)
        self.search_var = tk.StringVar()
        tk.Entry(right_frame, textvariable=self.search_var, width=28).grid(row=6, column=1,pady=5)
        
        # Buttons
        btns = tk.Frame(right_frame, bg="#A1E3F9")
        btns.grid(row=7, column=0, columnspan=2, padx=20, pady=10)
        tk.Button(btns, text="Add", command=self.on_add,bg="#3674B5",fg="white",width=7).grid(row=0, column=0, pady=2)
        tk.Button(btns, text="Update", command=self.on_update,bg="#3674B5",fg="white",width=7).grid(row=0, column=1,padx=5,pady=2)
        tk.Button(btns, text="Delete", command=self.on_delete,bg="#3674B5",fg="white",width=7).grid(row=0, column=2,padx=5,pady=2)
        tk.Button(btns, text="Find", command=self.on_search,bg="#3674B5",fg="white",width=7).grid(row=1, column=0,padx=5,pady=2)
        tk.Button(btns, text="Clear", command=self.clear_form,bg="#3674B5", fg="white", width=7).grid(row=1, column=1, padx=5, pady=2)
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
            self.tree.insert("", "end", values=(
                r["id"], r["name"], r["city"], r["country"], r.get("address", "")
            ), tags=(tag,))

    # ===================== SELECT ROW =====================
    def on_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        item = self.tree.item(sel[0])
        values = item["values"]
        _id, name, city, country, address = values

        self.name_var.set(name)
        self.addr_var.set(address)
        self.country_var.set(country)

        # Load cities theo country hiện tại
        country_id = self.country_map.get(country)
        if country_id:
            self.load_cities(country_id)
            # Chỉ set city nếu nó thực sự tồn tại trong danh sách mới
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
            messagebox.showinfo("Thành công", f"Đã thêm trường:\n{name}")
            self.refresh_list()
            self.clear_form()
        except IntegrityError as e:
            if e.errno == 1062:
                messagebox.showerror(
                    "Đã tồn tại",
                    f"Trường '{name}' đã có trong thành phố '{city_name}'!\nKhông thể thêm trùng."
                )
            else:
                messagebox.showerror("Lỗi CSDL", str(e))
        except Exception as e:
            messagebox.showerror("Lỗi không xác định", str(e))
    def on_update(self):
        uid = self.selected_id()
        if not uid:
            messagebox.showwarning("Warning", "Please select a university to update!")
            return

        name = self.name_var.get().strip()
        city_name = self.city_var.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "University name is required!")
            return
        if not city_name:
            messagebox.showwarning("Input Error", "Please select a city!")
            return

        city_id = self.city_map.get(city_name)
        if not city_id:
            messagebox.showerror("Error", "Invalid city selected!")
            return

        self.controller.update_university(uid, name, city_id, self.addr_var.get().strip() or None)
        self.refresh_list()
        self.clear_form()
        messagebox.showinfo("Success", "University updated successfully!")                    

    def on_delete(self):
        uid = self.selected_id()
        if not uid:
            messagebox.showwarning("Warning", "Please select a university to delete!")
            return
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this university?"):
            self.controller.delete_university(uid)
            self.refresh_list()
            self.clear_form()
            messagebox.showinfo("Success", "University deleted!")             
    def on_search(self):
        keyword = self.search_var.get().strip().lower()
        
        if not keyword:
            self.refresh_list()
            return
        
        all_rows = self.controller.get_all_universities()        
        # Tìm kiếm trên nhiều trường
        filtered = []
        for r in all_rows:
            if (keyword in r["name"].lower() or
                keyword in r["city"].lower() or
                keyword in r["country"].lower() or
                (r.get("address") and keyword in r["address"].lower())):
                filtered.append(r)
        # Xóa và hiển thị kết quả tìm kiếm với hiệu ứng so le màu
        self.tree.delete(*self.tree.get_children())
        self.tree.tag_configure("evenrow", background="white")
        self.tree.tag_configure("oddrow", background="#D1F8EF")
        
        for i, r in enumerate(filtered):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=(
                r["id"], r["name"], r["city"], r["country"], r.get("address", "")
            ), tags=(tag,))
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
        """Xóa trắng toàn bộ các ô nhập liệu trên form"""
        self.name_var.set("")
        self.addr_var.set("")
        self.country_var.set("")
        self.city_var.set("")
        self.search_var.set("")
        self.city_combo.configure(values=[])
        self.tree.selection_remove(self.tree.selection())
        self.tree.focus("")
        self.refresh_list()