import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from resource_utils import resource_path   # 🔥 Quan trọng

class MainView(tk.Frame):
    def __init__(self, master, controller, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.controller = controller
        master.configure(bg="#EAF2FF")
        master.title("International Education — Dashboard")

        self.setup_styles()
        self.pack(fill="both", expand=True, padx=12, pady=12)

        self.load_icons()
        self.create_header()
        self.create_admin_toolbar()
        self.create_controls()
        self.create_scroll_main()

    # ============================================================
    # STYLES
    # ============================================================
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Header.TFrame", background="#3674B5")
        style.configure("Header.TLabel", background="#3674B5", foreground="white",
                        font=("Segoe UI", 16, "bold"))

        style.configure("Card.TFrame", background="white")
        style.configure("CardTitle.TLabel", background="white", foreground="#222",
                        font=("Segoe UI", 11, "bold"))
        style.configure("Muted.TLabel", background="white", foreground="#666",
                        font=("Segoe UI", 9))

        style.configure("Accent.TButton",
                        background="#FFFFFF", foreground="#3674B5",
                        font=("Segoe UI", 10, "bold"))
        style.map("Accent.TButton",
                  background=[("active", "#3674B5")],
                  foreground=[("active", "#FFF")])

        style.configure("Treeview",
                        font=("Segoe UI", 10), rowheight=28,
                        background="white", foreground="#222")
        style.configure("Treeview.Heading",
                        font=("Segoe UI", 10, "bold"),
                        foreground="#3674B5", background="white")

    # ============================================================
    # ICONS (ĐÃ SỬA — DÙNG resource_path)
    # ============================================================
    def load_icons(self):
        def icon(path, size):
            full = resource_path(path)
            return ImageTk.PhotoImage(
                Image.open(full).resize(size, Image.Resampling.LANCZOS)
            )

        self.icons = {
            "country": icon("views/icons/country.png", (24, 24)),
            "city": icon("views/icons/building.png", (24, 24)),
            "university": icon("views/icons/university.png", (24, 24)),
            "program": icon("views/icons/setting.png", (24, 24)),
            "study": icon("views/icons/money.png", (24, 24)),
            "chart": icon("views/icons/chart.png", (20, 20)),
            "find": icon("views/icons/find.png", (20, 20)),
        }

    # ============================================================
    # HEADER
    # ============================================================
    def create_header(self):
        header = ttk.Frame(self, style="Header.TFrame", height=50)
        header.pack(fill="x")
        header.pack_propagate(False)

        left = ttk.Frame(header, style="Header.TFrame")
        left.pack(side="left", padx=16)
        ttk.Label(left, text="🌍", style="Header.TLabel").pack(side="left")
        ttk.Label(left, text=" International Study Costs", style="Header.TLabel").pack(side="left", padx=8)

        ttk.Label(header, text="Dashboard", style="Header.TLabel",
                  font=("Segoe UI", 10)).pack(side="right", padx=16)

    # ============================================================
    # ADMIN TOOLBAR
    # ============================================================
    def create_admin_toolbar(self):
        bar = ttk.Frame(self, style="Card.TFrame", padding=6)
        bar.pack(fill="x", pady=(6, 6))

        items = [
            ("Manage Country", "country"),
            ("Manage City", "city"),
            ("Manage University", "university"),
            ("Manage Program", "program"),
            ("Manage Study Cost", "study"),
        ]

        for i, (text, key) in enumerate(items):
            bar.grid_columnconfigure(i, weight=1)
            ttk.Button(bar, text=text, image=self.icons[key], compound="left",
                       style="Accent.TButton",
                       command=lambda n=text: self.controller.open_admin_window(n)
                       ).grid(row=0, column=i, sticky="nsew", padx=4)

    # ============================================================
    # CONTROLS
    # ============================================================
    def create_controls(self):
        frame = ttk.Frame(self, style="Card.TFrame", padding=12)
        frame.pack(fill="x")

        # Country
        cf = ttk.Frame(frame, style="Card.TFrame")
        cf.grid(row=0, column=0, padx=8, sticky="w")

        ttk.Label(cf, text="Country", image=self.icons["country"],
                  compound="left", font=("Segoe UI", 10, "bold"),
                  background="white").grid(row=0, column=0, padx=(0, 4))

        self.country_var = tk.StringVar()
        self.country_combo = ttk.Combobox(cf, textvariable=self.country_var,
                                          state="readonly", width=20)
        self.country_combo.grid(row=0, column=1)
        self.country_combo.bind("<<ComboboxSelected>>", self.on_country_selected)

        # Chart
        ch = ttk.Frame(frame, style="Card.TFrame")
        ch.grid(row=0, column=1, padx=8, sticky="w")

        ttk.Label(ch, text="Chart", image=self.icons["chart"],
                  compound="left", font=("Segoe UI", 10, "bold"),
                  background="white").grid(row=0, column=0, padx=(0, 4))

        self.chart_var = tk.StringVar()
        self.chart_combo = ttk.Combobox(
            ch, textvariable=self.chart_var, state="readonly", width=30,
            values=[
                "Average tuition by level",
                "Total yearly cost by university",
                "Average rent by city",
                "Number of programs by level",
                "Average living index by city",
                "Average total cost by program level",
                "Average tuition by program",
            ]
        )
        self.chart_combo.grid(row=0, column=1)
        self.chart_combo.current(0)

        ttk.Button(frame, text="Show", image=self.icons["find"], compound="left",
                   style="Accent.TButton",
                   command=self.on_show_chart_clicked
                   ).grid(row=0, column=2, padx=8)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

    # ============================================================
    # SCROLLING LAYOUT
    # ============================================================
    def create_scroll_main(self):
        outer = ttk.Frame(self)
        outer.pack(fill="both", expand=True)

        canvas = tk.Canvas(outer, bg="#EAF2FF", highlightthickness=0)
        scrollbar = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.scroll_frame = ttk.Frame(canvas, style="Card.TFrame")
        window = canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        self.scroll_frame.bind("<Configure>",
                               lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>",
                    lambda e: canvas.itemconfig(window, width=e.width))

        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        self.add_study_cost_section()
        self.add_tree()
        self.add_chart_section()

    # ============================================================
    # STUDY COST LABEL
    # ============================================================
    def add_study_cost_section(self):
        f = ttk.Frame(self.scroll_frame, style="Card.TFrame", padding=12)
        f.pack(anchor="w", pady=5)
        ttk.Label(f, text="Study costs", image=self.icons["study"],
                  compound="left", style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(f, text="List of universities & programs by selected country",
                  style="Muted.TLabel").pack(anchor="w")

    # ============================================================
    # TREEVIEW
    # ============================================================
    def add_tree(self):
        tf = ttk.Frame(self.scroll_frame, style="Card.TFrame", padding=12)
        tf.pack(fill="x", pady=6)

        frame = ttk.Frame(tf)
        frame.pack(fill="both", expand=True)

        cols = ("city", "university", "program", "level",
                "tuition", "rent", "visa", "insurance")

        self.tree = ttk.Treeview(frame, columns=cols, show="headings")
        headers = {
            "city": "City", "university": "University", "program": "Program",
            "level": "Level", "tuition": "Tuition (USD)", "rent": "Rent (USD)",
            "visa": "Visa fee (USD)", "insurance": "Insurance (USD)",
        }

        for c in cols:
            self.tree.heading(c, text=headers[c])
            self.tree.column(
                c,
                width=200 if c == "university" else 120,
                anchor="w"
            )

        scroll = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll.grid(row=0, column=1, sticky="ns")
        frame.grid_columnconfigure(0, weight=1)

        self.tree.tag_configure("oddrow", background="#FFFFFF")
        self.tree.tag_configure("evenrow", background="#F6FBFF")

        def _on_mousewheel(event):
            self.tree.yview_scroll(int(-1*(event.delta/120)), "units")
            return "break"

        self.tree.bind("<MouseWheel>", _on_mousewheel)

    # ============================================================
    # CHART AREA
    # ============================================================
    def add_chart_section(self):
        label_frame = ttk.Frame(self.scroll_frame, style="Card.TFrame", padding=12)
        label_frame.pack(anchor="w", pady=5)
        ttk.Label(label_frame, text="Visualizations", image=self.icons["chart"],
                  compound="left", style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(label_frame, text="Charts for selected country",
                  style="Muted.TLabel").pack(anchor="w")

        chart_f = ttk.Frame(self.scroll_frame, style="Card.TFrame", padding=12)
        chart_f.pack(fill="both")

        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("No chart selected")

        self.chart_canvas = FigureCanvasTkAgg(self.figure, master=chart_f)
        self.chart_canvas.get_tk_widget().pack(fill="both", expand=True)

    # ============================================================
    # DATA UPDATERS
    # ============================================================
    def set_countries(self, lst):
        names = [c["name"] for c in lst]
        self.country_combo["values"] = names
        if names and self.controller:
            self.country_combo.current(0)
            self.controller.on_country_changed(names[0])

    def clear_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

    def populate_tree(self, rows):
        self.clear_tree()
        for i, r in enumerate(rows):
            tag = "evenrow" if i % 2 else "oddrow"
            self.tree.insert("", "end",
                             values=(
                                 r.get("city", ""),
                                 r.get("university", ""),
                                 r.get("program", ""),
                                 r.get("level", ""),
                                 r.get("tuition_usd"),
                                 r.get("rent_usd"),
                                 r.get("visa_fee_usd"),
                                 r.get("insurance_usd"),
                             ), tags=(tag,))

    def show_chart(self, title, xl, yl, x_data, y_data):
        self.ax.clear()
        y = [0 if v is None else v for v in y_data]
        n = len(x_data)

        self.ax.bar(range(n), y, color="#3674B5", edgecolor="#578FCA")
        self.ax.set_title(title)
        self.ax.set_xlabel(xl)
        self.ax.set_ylabel(yl)
        self.ax.set_xticks(range(n))
        self.ax.set_xticklabels(
            x_data,
            rotation=45 if n > 5 else 0,
            ha="right" if n > 5 else "center"
        )

        self.ax.grid(axis="y", linestyle="--", color="#578FCA", alpha=0.3)
        self.figure.tight_layout()
        self.chart_canvas.draw_idle()

    # ============================================================
    # EVENTS
    # ============================================================
    def on_country_selected(self, _):
        if self.controller:
            self.controller.on_country_changed(self.country_var.get())

    def on_show_chart_clicked(self):
        if not self.country_var.get():
            return messagebox.showwarning("Missing country", "Please select a country")
        if not self.chart_var.get():
            return messagebox.showwarning("Missing chart", "Please select a chart type")

        self.controller.update_chart(self.country_var.get(), self.chart_var.get())
