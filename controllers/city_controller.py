from models.city_model import CityModel
from models.country_model import CountryModel
from mysql.connector.errors import IntegrityError


class CityController:
    def __init__(self):
        self.model = CityModel()
        self.country_model = CountryModel()

    def get_all_cities(self):
        return self.model.get_all_cities()

    def add_city(self, name, country_id, city_code=None):
        # Validate country_id exists first
        try:
            country_id_int = int(country_id)
        except (ValueError, TypeError):
            raise ValueError(f"Country ID '{country_id}' không hợp lệ! Vui lòng nhập số.")
        
        # Check if country exists
        country = self.country_model.get_country_by_id(country_id_int)
        if not country:
            raise ValueError(f"Quốc gia với ID '{country_id}' không tồn tại! Vui lòng kiểm tra lại Country ID.")
        
        country_name = country["name"]
        
        # Check if city already exists
        if self.model.city_exists(name, country_id_int):
            raise ValueError(f"Thành phố '{name}' đã tồn tại trong {country_name}! Không thể thêm trùng.")
        
        try:
            return self.model.create_city(name, country_id_int, city_code)
        except IntegrityError as e:
            if e.errno == 1062:
                # Duplicate entry
                raise ValueError(f"Thành phố '{name}' đã tồn tại trong {country_name}! Không thể thêm trùng.")
            elif e.errno == 1452:
                # Foreign key constraint fails
                raise ValueError(f"Quốc gia với ID '{country_id}' không tồn tại! Vui lòng kiểm tra lại Country ID.")
            else:
                raise ValueError(f"Lỗi khi thêm thành phố: {str(e)}")
        except Exception as e:
            error_str = str(e)
            if "1452" in error_str or "foreign key" in error_str.lower() or "fk_cities_country" in error_str:
                raise ValueError(f"Quốc gia với ID '{country_id}' không tồn tại! Vui lòng kiểm tra lại Country ID.")
            raise ValueError(f"Không thể thêm thành phố: {error_str}")

    def update_city(self, city_id, name=None, country_id=None, city_code=None):
        return self.model.update_city(
            city_id,
            name=name,
            country_id=country_id,
            city_code=city_code
        )

    def delete_city(self, city_id):
        return self.model.delete_city(city_id)

    def search_city(self, keyword=None, country_id=None):
        rows = self.get_all_cities()
        if not keyword and not country_id:
            return rows

        def match(row):
            by_keyword = True
            if keyword:
                by_keyword = keyword.lower() in row["city"].lower()

            by_country = True
            if country_id:
                by_country = row["country_id"] == country_id

            return by_keyword and by_country

        return [row for row in rows if match(row)]

    def get_countries(self):
        return self.country_model.get_all_countries()