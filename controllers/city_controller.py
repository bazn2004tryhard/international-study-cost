from models.city_model import CityModel
from models.country_model import CountryModel


class CityController:
    def __init__(self, main_controller=None):
        self.model = CityModel()
        self.country_model = CountryModel()

    def get_all_cities(self):
        return self.model.get_all_cities()

    def add_city(self, name, country_id, city_code=None):
        return self.model.create_city(name, country_id, city_code)

    def update_city(self, city_id, name=None, country_id=None, city_code=None):
        return self.model.update_city(city_id, name=name, country_id=country_id, city_code=city_code)

    def delete_city(self, city_id):
        return self.model.delete_city(city_id)

    def search_city(self, keyword, country_id=None):
        rows = self.get_all_cities()
        if not keyword and not country_id:
            return rows

        def match(row):
            matches_keyword = True
            if keyword:
                matches_keyword = keyword.lower() in row["city"].lower()

            matches_country = True
            if country_id:
                matches_country = row["country_id"] == country_id

            return matches_keyword and matches_country

        return [row for row in rows if match(row)]