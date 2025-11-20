from models.city_model import CityModel
from models.country_model import CountryModel

class CityController:
    def __init__(self, main_controller=None):
        self.model = CityModel()
        self.country_model = CountryModel()