from models.studycost_model import StudyCostModel
from models.country_model import CountryModel
from models.city_model import CityModel
from models.university_model import UniversityModel
from models.program_model import ProgramModel


class StudyCostController:

    def __init__(self):
        self.cost_model = StudyCostModel()
        self.country_model = CountryModel()
        self.city_model = CityModel()
        self.university_model = UniversityModel()
        self.program_model = ProgramModel()

    # ============================================================
    # DATA HELPERS (Dropdowns)
    # ============================================================
    def get_countries(self):
        return self.country_model.get_all_countries()

    def get_cities_by_country(self, country_id):
        return self.city_model.get_cities_by_country(country_id)

    def get_universities_by_city(self, city_id):
        return self.university_model.get_universities_by_city(city_id)

    def get_all_programs(self):
        return self.program_model.get_all_programs()

    # ============================================================
    # CRUD
    # ============================================================
    def get_costs_by_country(self, country_id):
        return self.cost_model.get_costs_by_country(country_id)

    def get_costs_by_university(self, university_id):
        return self.cost_model.get_costs_by_university(university_id)

    def add_cost(
        self,
        university_id,
        program_id,
        duration_years,
        tuition_usd,
        living_cost_index,
        rent_usd,
        visa_fee_usd,
        insurance_usd,
        exchange_rate,
    ):
        return self.cost_model.create_cost(
            university_id,
            program_id,
            duration_years,
            tuition_usd,
            living_cost_index,
            rent_usd,
            visa_fee_usd,
            insurance_usd,
            exchange_rate,
        )

    def update_cost(self, cost_id, **kwargs):
        return self.cost_model.update_cost(cost_id, **kwargs)

    def delete_cost(self, cost_id):
        return self.cost_model.delete_cost(cost_id)

    def search_costs(self, country_id=None, university_id=None):
        """
        Tìm kiếm chi phí.
        Nếu có university_id -> ưu tiên tìm theo trường.
        Nếu chỉ có country_id -> tìm theo quốc gia.
        """
        if university_id:
            return self.get_costs_by_university(university_id)
        if country_id:
            return self.get_costs_by_country(country_id)
        return []
