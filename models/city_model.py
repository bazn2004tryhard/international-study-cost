from .base_model import BaseModel


class CityModel(BaseModel):

    # ============================================================
    # READ
    # ============================================================
    def get_all_cities(self):
        query = """
            SELECT 
                ci.id,
                ci.name AS city,
                ci.city_code,
                ci.country_id,
                c.name AS country
            FROM cities ci
            JOIN countries c ON ci.country_id = c.id
            ORDER BY ci.name
        """
        return self.execute_query(query, fetchall=True)

    def get_city_by_id(self, city_id):
        query = """
            SELECT 
                ci.id,
                ci.name,
                ci.city_code,
                ci.country_id,
                c.name AS country
            FROM cities ci
            JOIN countries c ON ci.country_id = c.id
            WHERE ci.id = %s
        """
        return self.execute_query(query, (city_id,), fetchone=True)

    def get_cities_by_country(self, country_id):
        query = """
            SELECT 
                id,
                name,
                city_code,
                country_id
            FROM cities
            WHERE country_id = %s
            ORDER BY name
        """
        return self.execute_query(query, (country_id,), fetchall=True)

    # ============================================================
    # CREATE
    # ============================================================
    def create_city(self, name, country_id, city_code=None):
        query = """
            INSERT INTO cities (name, country_id, city_code)
            VALUES (%s, %s, %s)
        """
        return self.execute_insert(query, (name, country_id, city_code))

    # ============================================================
    # UPDATE
    # ============================================================
    def update_city(self, city_id, name=None, country_id=None, city_code=None):
        fields = []
        values = []

        if name:
            fields.append("name = %s")
            values.append(name)

        if country_id:
            fields.append("country_id = %s")
            values.append(country_id)

        if city_code:
            fields.append("city_code = %s")
            values.append(city_code)

        if not fields:
            return 0

        query = f"UPDATE cities SET {', '.join(fields)} WHERE id = %s"
        values.append(city_id)

        return self.execute_non_query(query, tuple(values))

    # ============================================================
    # DELETE
    # ============================================================
    def delete_city(self, city_id):
        query = "DELETE FROM cities WHERE id = %s"
        return self.execute_non_query(query, (city_id,))
