# models/city_model.py
from .base_model import BaseModel


class CityModel(BaseModel):

    # READ
    def get_all_cities(self):
        """
        Lấy tất cả thành phố + quốc gia.
        """
        query = """
        SELECT 
            ci.id,
            ci.name AS city,
            c.name AS country,
            c.id AS country_id
        FROM cities ci
        JOIN countries c ON ci.country_id = c.id
        ORDER BY c.name, ci.name
        """
        return self.execute_query(query, fetchall=True)

    def get_city_by_id(self, city_id: int):
        """
        Lấy 1 thành phố theo ID.
        """
        query = """
        SELECT 
            ci.id,
            ci.name AS city,
            c.id AS country_id,
            c.name AS country
        FROM cities ci
        JOIN countries c ON ci.country_id = c.id
        WHERE ci.id = %s
        """
        return self.execute_query(query, (city_id,), fetchone=True)

    def get_cities_by_country(self, country_id: int):
        """
        Lấy danh sách city theo country ID.
        """
        query = """
        SELECT id, name 
        FROM cities 
        WHERE country_id = %s
        ORDER BY name
        """
        return self.execute_query(query, (country_id,), fetchall=True)

    # CREATE
    def create_city(self, name: str, country_id: int) -> int:
        """
        Thêm city mới.
        Trả về id được tạo.
        """
        query = """
        INSERT INTO cities (name, country_id)
        VALUES (%s, %s)
        """
        return self.execute_insert(query, (name, country_id))

    # UPDATE
    def update_city(self, city_id: int, name: str = None, country_id: int = None) -> int:
        """
        Cập nhật linh hoạt theo tham số truyền vào.
        Ví dụ:
            update_city(5, name="Tokyo")
            update_city(3, country_id=2)
            update_city(7, name="Paris", country_id=4)
        """
        fields = []
        params = []

        if name is not None:
            fields.append("name = %s")
            params.append(name)

        if country_id is not None:
            fields.append("country_id = %s")
            params.append(country_id)

        if not fields:
            return 0

        params.append(city_id)

        query = f"UPDATE cities SET {', '.join(fields)} WHERE id = %s"
        return self.execute_non_query(query, tuple(params))

    # DELETE
    def delete_city(self, city_id: int) -> int:
        """
        Xóa 1 city (CASCADE sẽ tự xóa university liên quan nếu set trong DB).
        """
        query = "DELETE FROM cities WHERE id = %s"
        return self.execute_non_query(query, (city_id,))
