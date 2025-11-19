# controllers/main_controller.py
import tkinter.messagebox as messagebox
from models.country_model import CountryModel
from models.base_model import BaseModel


class MainController:
    def __init__(self, view):
        self.view = view
        self.country_model = CountryModel()
        self.base_model = BaseModel()  # dùng tạm để query join cho màn hình chính

        self.load_initial_data()

    def load_initial_data(self):
        try:
            countries = self.country_model.get_all_countries()
            if not countries:
                countries = []
            self.view.set_countries(countries)
            self.countries = {c["name"]: c["id"] for c in countries}
        except Exception as e:
            messagebox.showerror("Database Error", f"Cannot load countries:\n{e}")
            self.countries = {}

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
            if not rows:
                rows = []
            self.view.populate_tree(rows)
        except Exception as e:
            messagebox.showerror("Database Error", f"Query failed:\n{e}")
            self.view.clear_tree()
