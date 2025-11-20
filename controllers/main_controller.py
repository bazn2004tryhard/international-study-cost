import tkinter.messagebox as messagebox

# Model cho màn hình chính
from models.country_model import CountryModel
from models.base_model import BaseModel
from models.studycost_model import StudyCostModel

# Import các VIEW quản lý
from views.manage_country_view import ManageCountryWindow
from views.manage_city_view import ManageCityWindow
from views.manage_program_view import ManageProgramWindow
from views.manage_university_view import ManageUniversityWindow
from views.manage_studycost_view import ManageStudyCostWindow

# Import các CONTROLLER quản lý
from controllers.country_controller import CountryController
from controllers.city_controller import CityController
from controllers.program_controller import ProgramController
from controllers.university_controller import UniversityController
from controllers.studycost_controller import StudyCostController


class MainController:

    def __init__(self, view):
        self.view = view

        # MODEL dùng cho màn hình chính
        self.country_model = CountryModel()
        self.base_model = BaseModel()
        self.study_cost_model = StudyCostModel()

        # MAP Country name → id
        self.countries = {}

        self.load_initial_data()

    # ============================================================
    # LOAD COUNTRY CHO MÀN HÌNH CHÍNH
    # ============================================================
    def load_initial_data(self):
        try:
            countries = self.country_model.get_all_countries()
            self.countries = {c["name"]: c["id"] for c in countries}
            self.view.set_countries(countries)
        except Exception as e:
            messagebox.showerror("Database Error", f"Cannot load countries:\n{e}")

    # ============================================================
    # KHI CHỌN COUNTRY — LOAD DỮ LIỆU BẢNG
    # ============================================================
    def on_country_changed(self, country_name):
        country_id = self.countries.get(country_name)
        if not country_id:
            return

        query = """
        SELECT 
            ci.name AS city,
            u.name  AS university,
            p.name  AS program,
            p.level AS level,
            s.tuition_usd,
            s.rent_usd,
            s.visa_fee_usd,
            s.insurance_usd
        FROM study_costs s
        JOIN universities u ON s.university_id = u.id
        JOIN cities ci      ON u.city_id = ci.id
        JOIN countries c    ON ci.country_id = c.id
        JOIN programs p     ON s.program_id = p.id
        WHERE c.id = %s
        ORDER BY ci.name, u.name, p.name;
        """

        try:
            rows = self.base_model.execute_query(query, (country_id,), fetchall=True)
            self.view.populate_tree(rows or [])
        except Exception as e:
            messagebox.showerror("Query Error", f"Cannot load data:\n{e}")
            self.view.clear_tree()

    # ============================================================
    # MỞ CỬA SỔ QUẢN LÝ ADMIN
    # ============================================================
    def open_admin_window(self, choice):
        """
        choice là text từ combobox admin.
        Mỗi mục mở 1 WINDOW + 1 CONTROLLER tương ứng.
        """

        if choice == "Manage Country":
            controller = CountryController()
            ManageCountryWindow(self.view.master, controller)

        elif choice == "Manage City":
            controller = CityController()
            ManageCityWindow(self.view.master, controller)

        elif choice == "Manage Program":
            controller = ProgramController()
            ManageProgramWindow(self.view.master, controller)

        elif choice == "Manage University":
            controller = UniversityController()
            ManageUniversityWindow(self.view.master, controller)

        elif choice == "Manage Study Cost":
            controller = StudyCostController()
            ManageStudyCostWindow(self.view.master, controller)

        else:
            messagebox.showinfo("Not implemented", f"{choice} window is not implemented.")

    # ============================================================
    # XỬ LÝ BIỂU ĐỒ
    # ============================================================
    def update_chart(self, country_name, chart_type):
        country_id = self.countries.get(country_name)
        if not country_id:
            return

        try:
            if chart_type == "Average tuition by level":
                data = self.study_cost_model.get_tuition_by_university_and_level(country_id)
                levels = sorted({row["level"] for row in data})
                avg = []
                for lvl in levels:
                    values = [r["avg_tuition"] for r in data if r["level"] == lvl]
                    avg.append(sum(values) / len(values))
                self.view.show_chart("Tuition by level", "Level", "Tuition USD", levels, avg)

            elif chart_type == "Total yearly cost by university":
                data = self.study_cost_model.get_total_cost_by_university(country_id)
                x = [row["university"] for row in data]
                y = [float(row["avg_total_cost"] or 0) for row in data]
                self.view.show_chart("Total yearly cost", "University", "Cost USD", x, y)

            elif chart_type == "Average rent by city":
                data = self.study_cost_model.get_avg_rent_by_city(country_id)
                x = [row["city"] for row in data]
                y = [float(row["avg_rent"] or 0) for row in data]
                self.view.show_chart("Average rent", "City", "Rent USD", x, y)

            elif chart_type == "Number of programs by level":
                data = self.study_cost_model.get_program_count_by_level(country_id)
                x = [row["level"] for row in data]
                y = [int(row["program_count"]) for row in data]
                self.view.show_chart("Program count", "Level", "Count", x, y)

        except Exception as e:
            messagebox.showerror("Chart error", str(e))
