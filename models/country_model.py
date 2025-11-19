# models/country_model.py
from .base_model import BaseModel


class CountryModel(BaseModel):

    # READ
    def get_all_countries(self):
        query = "SELECT id, name FROM countries ORDER BY name"
        return self.execute_query(query, fetchall=True)

    def get_country_by_id(self, country_id: int):
        query = "SELECT id, name FROM countries WHERE id = %s"
        return self.execute_query(query, (country_id,), fetchone=True)

    def get_country_by_name(self, name: str):
        query = "SELECT id, name FROM countries WHERE name = %s"
        return self.execute_query(query, (name,), fetchone=True)

    # CREATE
    def create_country(self, name: str) -> int:
        """
        Tạo country mới, trả về id.
        """
        query = "INSERT INTO countries (name) VALUES (%s)"
        return self.execute_insert(query, (name,))

    # UPDATE
    def update_country(self, country_id: int, new_name: str) -> int:
        """
        Cập nhật tên country, trả về số dòng bị ảnh hưởng.
        """
        query = "UPDATE countries SET name = %s WHERE id = %s"
        return self.execute_non_query(query, (new_name, country_id))

    # DELETE
    def delete_country(self, country_id: int) -> int:
        """
        Xóa country theo id (cascade sẽ xóa luôn city, university, cost nếu có FK ON DELETE CASCADE).
        """
        query = "DELETE FROM countries WHERE id = %s"
        return self.execute_non_query(query, (country_id,))
