from .base_model import BaseModel

class CountryModel(BaseModel):

    # READ
    def get_all_countries(self):
        query = """
            SELECT 
                id,
                name,
                country_code,
                population,
                currency
            FROM countries 
            ORDER BY name
        """
        return self.execute_query(query, fetchall=True)

    def get_country_by_id(self, country_id: int):
        query = """
            SELECT 
                id,
                name,
                country_code,
                population,
                currency
            FROM countries 
            WHERE id = %s
        """
        return self.execute_query(query, (country_id,), fetchone=True)

    # CREATE
    def create_country(self, name: str, code: str, population: int, currency: str) -> int:
        query = """
            INSERT INTO countries (name, country_code, population, currency)
            VALUES (%s, %s, %s, %s)
        """
        return self.execute_insert(query, (name, code, population, currency))

    # UPDATE
    def update_country(self, country_id: int, name: str, code: str, population: int, currency: str) -> int:
        query = """
            UPDATE countries 
            SET 
                name = %s,
                country_code = %s,
                population = %s,
                currency = %s
            WHERE id = %s
        """
        return self.execute_non_query(query, (name, code, population, currency, country_id))

    # DELETE
    def delete_country(self, country_id: int) -> int:
        query = "DELETE FROM countries WHERE id = %s"
        return self.execute_non_query(query, (country_id,))
