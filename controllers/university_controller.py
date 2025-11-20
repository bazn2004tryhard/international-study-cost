from models.university_model import UniversityModel
from models.country_model import CountryModel
from models.city_model import CityModel

class UniversityController:
    def __init__(self):
        self.model = UniversityModel()
        self.country_model = CountryModel()
        self.city_model = CityModel()