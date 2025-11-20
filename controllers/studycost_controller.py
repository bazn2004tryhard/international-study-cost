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