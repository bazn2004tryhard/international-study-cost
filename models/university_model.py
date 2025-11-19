# models/university_model.py
from .base_model import BaseModel


class UniversityModel(BaseModel):

    # READ
    def get_all_universities(self):
        query = """
        SELECT u.id, u.name, ci.name AS city, c.name AS country
        FROM universities u
        JOIN cities ci ON u.city_id = ci.id
        JOIN countries c ON ci.country_id = c.id
        ORDER BY c.name, ci.name, u.name
        """
        return self.execute_query(query, fetchall=True)

    def get_university_by_id(self, university_id: int):
        query = """
        SELECT u.id, u.name, u.city_id, ci.name AS city, c.name AS country
        FROM universities u
        JOIN cities ci ON u.city_id = ci.id
        JOIN countries c ON ci.country_id = c.id
        WHERE u.id = %s
        """
        return self.execute_query(query, (university_id,), fetchone=True)

    def get_universities_by_city(self, city_id: int):
        query = "SELECT id, name, city_id FROM universities WHERE city_id = %s ORDER BY name"
        return self.execute_query(query, (city_id,), fetchall=True)

    # CREATE
    def create_university(self, name: str, city_id: int) -> int:
        query = "INSERT INTO universities (name, city_id) VALUES (%s, %s)"
        return self.execute_insert(query, (name, city_id))

    # UPDATE
    def update_university(self, university_id: int, name: str = None, city_id: int = None) -> int:
        """
        Cập nhật linh hoạt; truyền tham số nào thì update tham số đó.
        """
        fields = []
        params = []

        if name is not None:
            fields.append("name = %s")
            params.append(name)
        if city_id is not None:
            fields.append("city_id = %s")
            params.append(city_id)

        if not fields:
            return 0  # không có gì để update

        params.append(university_id)
        query = f"UPDATE universities SET {', '.join(fields)} WHERE id = %s"
        return self.execute_non_query(query, tuple(params))

    # DELETE
    def delete_university(self, university_id: int) -> int:
        query = "DELETE FROM universities WHERE id = %s"
        return self.execute_non_query(query, (university_id,))
