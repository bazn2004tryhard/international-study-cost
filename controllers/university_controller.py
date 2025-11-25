from models.university_model import UniversityModel
from models.country_model import CountryModel
from models.city_model import CityModel


class UniversityController:
    def __init__(self):
        self.model = UniversityModel()
        self.country_model = CountryModel()
        self.city_model = CityModel()

    def get_all_universities(self):
        return self.model.get_all_universities()

    def get_university(self, university_id):
        return self.model.get_university_by_id(university_id)

    def add_university(self, name, city_id, address=None):
        return self.model.create_university(name, city_id, address)

    def update_university(self, university_id, name=None, city_id=None, address=None):
        return self.model.update_university(
            university_id,
            name=name,
            city_id=city_id,
            address=address
        )

    def delete_university(self, university_id):
        return self.model.delete_university(university_id)

    def search_university(self, keyword=None, country_id=None, city_id=None):
        rows = self.get_all_universities()
        if not keyword and not country_id and not city_id:
            return rows

        def match(row):
            by_keyword = True
            if keyword:
                by_keyword = keyword.lower() in row["name"].lower()

            by_country = True
            if country_id:
                by_country = row["country_id"] == country_id

            by_city = True
            if city_id:
                by_city = row["city_id"] == city_id

            return by_keyword and by_country and by_city

        return [row for row in rows if match(row)]

    def get_countries(self):
        return self.country_model.get_all_countries()

    def get_cities_by_country(self, country_id):
        return self.city_model.get_cities_by_country(country_id)