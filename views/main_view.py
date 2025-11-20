import tkinter as tk
from tkinter import ttk, messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class MainView(tk.Frame):
    def __init__(self, master, controller, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.controller = controller

        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        # ---------- TOP AREA ----------
        top_frame = ttk.Frame(self)
        top_frame.pack(side="top", fill="x", padx=10, pady=10)

        # Country combobox
        ttk.Label(top_frame, text="Country").grid(row=0, column=0, sticky="w")
        self.country_var = tk.StringVar()
        self.country_combo = ttk.Combobox(
            top_frame, textvariable=self.country_var, state="readonly"
        )
        self.country_combo.grid(row=0, column=1, padx=5, sticky="ew")
        self.country_combo.bind("<<ComboboxSelected>>", self.on_country_selected)

        # Admin combobox (open manage windows)
        ttk.Label(top_frame, text="Admin").grid(row=0, column=2, padx=(20, 0), sticky="w")
        self.admin_var = tk.StringVar()
        self.admin_combo = ttk.Combobox(
            top_frame,
            textvariable=self.admin_var,
            state="readonly",
            values=[
                "Manage Country",
                "Manage City",
                "Manage University",
                "Manage Program",
                "Manage Study Cost",
            ],
        )
        self.admin_combo.grid(row=0, column=3, padx=5, sticky="ew")
        self.admin_combo.bind("<<ComboboxSelected>>", self.on_admin_selected)

        # Chart combobox
        ttk.Label(top_frame, text="Show charts").grid(
            row=0, column=4, padx=(20, 0), sticky="w"
        )
        self.chart_var = tk.StringVar()
        self.chart_combo = ttk.Combobox(
            top_frame,
            textvariable=self.chart_var,
            state="readonly",
            values=[
                "Average tuition by level",
                "Total yearly cost by university",
                "Average rent by city",
                "Number of programs by level",
            ],
        )
        self.chart_combo.grid(row=0, column=5, padx=5, sticky="ew")

        self.btn_show_chart = ttk.Button(
            top_frame, text="Show", command=self.on_show_chart_clicked
        )
        self.btn_show_chart.grid(row=0, column=6, padx=(10, 0))

        top_frame.grid_columnconfigure(1, weight=1)
        top_frame.grid_columnconfigure(3, weight=1)
        top_frame.grid_columnconfigure(5, weight=1)

        # ---------- MIDDLE: TABLE ----------
        middle_frame = ttk.Frame(self)
        middle_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(0, 5))

        columns = (
            "city",
            "university",
            "program",
            "level",
            "tuition",
            "rent",
            "visa",
            "insurance",
        )
        self.tree = ttk.Treeview(
            middle_frame, columns=columns, show="headings", height=10
        )
        headings = {
            "city": "City",
            "university": "University",
            "program": "Program",
            "level": "Level",
            "tuition": "Tuition (USD)",
            "rent": "Rent (USD)",
            "visa": "Visa fee (USD)",
            "insurance": "Insurance (USD)",
        }
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=120, anchor="w")

        vsb = ttk.Scrollbar(middle_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        middle_frame.grid_rowconfigure(0, weight=1)
        middle_frame.grid_columnconfigure(0, weight=1)

        # ---------- BOTTOM: CHART AREA ----------
        bottom_frame = ttk.LabelFrame(self, text="Chart")
        bottom_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(0, 10))

        self.figure = Figure(figsize=(8, 3), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("No chart")
        self.ax.set_xlabel("")
        self.ax.set_ylabel("")

        self.canvas = FigureCanvasTkAgg(self.figure, master=bottom_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    # ---------- Public methods for controller ----------

    def set_countries(self, country_list):
        names = [c["name"] for c in country_list]
        self.country_combo["values"] = names
        if names:
            self.country_combo.current(0)
            # load luôn country đầu tiên
            if self.controller:
                self.controller.on_country_changed(names[0])

    def clear_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def populate_tree(self, rows):
        self.clear_tree()
        for row in rows:
            self.tree.insert(
                "",
                "end",
                values=(
                    row.get("city", ""),
                    row.get("university", ""),
                    row.get("program", ""),
                    row.get("level", ""),
                    row.get("tuition_usd"),
                    row.get("rent_usd"),
                    row.get("visa_fee_usd"),
                    row.get("insurance_usd"),
                ),
            )

    def show_chart(self, title, x_label, y_label, x_data, y_data):
        self.ax.clear()
        self.ax.bar(x_data, y_data)
        self.ax.set_title(title)
        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)
        self.figure.tight_layout()
        self.canvas.draw_idle()

    # ---------- Event handlers ----------

    def on_country_selected(self, event):
        if not self.controller:
            return
        name = self.country_var.get()
        if name:
            self.controller.on_country_changed(name)

    def on_admin_selected(self, event):
        if not self.controller:
            return
        choice = self.admin_var.get()
        self.controller.open_admin_window(choice)

    def on_show_chart_clicked(self):
        if not self.controller:
            return
        country_name = self.country_var.get()
        chart_type = self.chart_var.get()
        if not country_name:
            messagebox.showwarning("Missing country", "Please select a country first.")
            return
        if not chart_type:
            messagebox.showwarning("Missing chart", "Please select a chart type.")
            return
        self.controller.update_chart(country_name, chart_type)

