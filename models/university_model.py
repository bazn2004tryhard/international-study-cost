from .base_model import BaseModel


class UniversityModel(BaseModel):

    # ============================================================
    # READ
    # ============================================================
    def get_all_universities(self):
        query = """
            SELECT 
                u.id,
                u.name,
                u.address,
                ci.name AS city,
                ci.id AS city_id,
                c.name AS country,
                c.id AS country_id
            FROM universities u
            JOIN cities ci ON u.city_id = ci.id
            JOIN countries c ON ci.country_id = c.id
            ORDER BY u.name
        """
        return self.execute_query(query, fetchall=True)

    def get_university_by_id(self, university_id):
        query = """
            SELECT 
                u.id,
                u.name,
                u.address,
                u.city_id,
                ci.name AS city,
                c.name AS country
            FROM universities u
            JOIN cities ci ON u.city_id = ci.id
            JOIN countries c ON ci.country_id = c.id
            WHERE u.id = %s
        """
        return self.execute_query(query, (university_id,), fetchone=True)

    def get_universities_by_city(self, city_id):
        query = """
            SELECT 
                id,
                name,
                address,
                city_id
            FROM universities
            WHERE city_id = %s
            ORDER BY name
        """
        return self.execute_query(query, (city_id,), fetchall=True)

    # ============================================================
    # CREATE
    # ============================================================
    def create_university(self, name, city_id, address=None):
        query = """
            INSERT INTO universities (name, city_id, address)
            VALUES (%s, %s, %s)
        """
        return self.execute_insert(query, (name, city_id, address))

    # ============================================================
    # UPDATE
    # ============================================================
    def update_university(self, university_id, name=None, city_id=None, address=None):
        fields = []
        values = []

        if name:
            fields.append("name = %s")
            values.append(name)

        if city_id:
            fields.append("city_id = %s")
            values.append(city_id)

        if address:
            fields.append("address = %s")
            values.append(address)

        if not fields:
            return 0

        query = f"UPDATE universities SET {', '.join(fields)} WHERE id = %s"
        values.append(university_id)

        return self.execute_non_query(query, tuple(values))

    # ============================================================
    # DELETE
    # ============================================================
    def delete_university(self, university_id):
        query = "DELETE FROM universities WHERE id = %s"
        return self.execute_non_query(query, (university_id,))
