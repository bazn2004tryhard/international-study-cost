from models.country_model import CountryModel

class CountryController:
    def __init__(self):
        self.model = CountryModel()

    def get_all_countries(self):
        return self.model.get_all_countries()

    def add_country(self, name, code, population, currency):
        return self.model.create_country(name, code, population, currency)

    def update_country(self, cid, name, code, population, currency):
        return self.model.update_country(cid, name, code, population, currency)

    def delete_country(self, cid):
        return self.model.delete_country(cid)

    def search_country(self, keyword):
        rows = self.get_all_countries()
        if not keyword:
            return rows
        return [r for r in rows if keyword.lower() in r["name"].lower()]
