from models.country_model import CountryModel
from mysql.connector.errors import IntegrityError

class CountryController:
    def __init__(self):
        self.model = CountryModel()

    def get_all_countries(self):
        return self.model.get_all_countries()

    def add_country(self, name, code, population, currency):
        if not name or not name.strip():
            raise ValueError("Tên quốc gia không được để trống!")
        try:
            return self.model.create_country(name.strip(), code, population, currency)
        except IntegrityError as e:
            if e.errno == 1062:
                raise ValueError(f"Quốc gia '{name.strip()}' đã tồn tại! Không thể thêm trùng.")
            raise ValueError(f"Lỗi khi thêm quốc gia: {str(e)}")
        except Exception as e:
            raise ValueError(f"Không thể thêm quốc gia: {str(e)}")

    def update_country(self, cid, name, code, population, currency):
        if not name or not name.strip():
            raise ValueError("Tên quốc gia không được để trống!")
        try:
            return self.model.update_country(cid, name.strip(), code, population, currency)
        except IntegrityError as e:
            if e.errno == 1062:
                raise ValueError(f"Quốc gia '{name.strip()}' đã tồn tại! Không thể cập nhật trùng.")
            raise ValueError(f"Lỗi khi cập nhật quốc gia: {str(e)}")
        except Exception as e:
            raise ValueError(f"Không thể cập nhật quốc gia: {str(e)}")

    def delete_country(self, cid):
        return self.model.delete_country(cid)

    def search_country(self, keyword):
        rows = self.get_all_countries()
        if not keyword:
            return rows
        return [r for r in rows if keyword.lower() in r["name"].lower()]
