from models.studycost_model import StudyCostModel
from models.country_model import CountryModel
from models.city_model import CityModel
from models.university_model import UniversityModel
from models.program_model import ProgramModel


class StudyCostController:

    def __init__(self):
        self.model = StudyCostModel()   # đổi lại cho đồng bộ
        self.country_model = CountryModel()
        self.city_model = CityModel()
        self.university_model = UniversityModel()
        self.program_model = ProgramModel()

    def get_all_study_costs(self):
        return self.model.get_all_study_costs()
    def get_cost_by_id(self, cost_id):
        """Lấy 1 bản ghi study_cost theo ID (dùng cho on_select)"""
        return self.model.get_cost_by_id(cost_id)

    def add_study_cost(self, university_id, program_id, level, duration,
                       tuition, rent, visa, insurance, exchange):
        return self.model.create_study_cost(
            university_id, program_id, level, duration,
            tuition, rent, visa, insurance, exchange
        )
    def update_study_cost(self, cost_id, university_id=None, program_id=None,
                          level=None, duration=None, tuition=None, rent=None,
                          visa=None, insurance=None, exchange=None):
        return self.model.update_study_cost(
            cost_id,
            university_id=university_id,
            program_id=program_id,
            level=level,
            duration=duration,
            tuition=tuition,
            rent=rent,
            visa=visa,
            insurance=insurance,
            exchange=exchange
        )

    def delete_study_cost(self, cost_id):
        return self.model.delete_study_cost(cost_id)

    def search_study_cost(self, keyword=None, university_id=None, program_id=None):
        rows = self.get_all_study_costs()
        if not keyword and not university_id and not program_id:
            return rows

        def match(row):
            by_keyword = True
            if keyword:
                by_keyword = (
                    keyword.lower() in row["program"].lower()
                    or keyword.lower() in row["university"].lower()
                )

            by_university = True
            if university_id:
                by_university = row["university_id"] == university_id

            by_program = True
            if program_id:
                by_program = row["program_id"] == program_id

            return by_keyword and by_university and by_program

        return [row for row in rows if match(row)]

    def get_countries(self):
        return self.country_model.get_all_countries()

    def get_cities_by_country(self, country_id):
        return self.city_model.get_cities_by_country(country_id)

    def get_universities(self):
        return self.university_model.get_all_universities()

    def get_programs(self):
        return self.program_model.get_all_programs()
