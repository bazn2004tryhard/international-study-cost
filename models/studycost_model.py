# models/studycost_model.py
from .base_model import BaseModel


class StudyCostModel(BaseModel):

    # READ
    def get_cost_by_id(self, cost_id: int):
        query = """
        SELECT 
            s.id,
            s.duration_years,
            s.tuition_usd,
            s.living_cost_index,
            s.rent_usd,
            s.visa_fee_usd,
            s.insurance_usd,
            s.exchange_rate,
            u.id AS university_id,
            u.name AS university,
            ci.name AS city,
            c.name AS country,
            p.id AS program_id,
            p.name AS program,
            p.level AS level
        FROM study_costs s
        JOIN universities u ON s.university_id = u.id
        JOIN cities ci      ON u.city_id = ci.id
        JOIN countries c    ON ci.country_id = c.id
        JOIN programs p     ON s.program_id = p.id
        WHERE s.id = %s
        """
        return self.execute_query(query, (cost_id,), fetchone=True)

    def get_costs_by_university(self, university_id: int):
        query = """
        SELECT 
            s.id,
            p.name AS program,
            p.level AS level,
            s.duration_years,
            s.tuition_usd,
            s.rent_usd,
            s.visa_fee_usd,
            s.insurance_usd,
            s.living_cost_index
        FROM study_costs s
        JOIN programs p ON s.program_id = p.id
        WHERE s.university_id = %s
        ORDER BY p.level, p.name
        """
        return self.execute_query(query, (university_id,), fetchall=True)

    def get_costs_by_country(self, country_id: int):
        """
        Truy vấn chi phí theo country (dùng join).
        """
        query = """
        SELECT 
            c.name AS country,
            ci.name AS city,
            u.name AS university,
            p.name AS program,
            p.level AS level,
            s.id,
            s.duration_years,
            s.tuition_usd,
            s.living_cost_index,
            s.rent_usd,
            s.visa_fee_usd,
            s.insurance_usd,
            s.exchange_rate
        FROM study_costs s
        JOIN universities u ON s.university_id = u.id
        JOIN cities ci      ON u.city_id = ci.id
        JOIN countries c    ON ci.country_id = c.id
        JOIN programs p     ON s.program_id = p.id
        WHERE c.id = %s
        ORDER BY ci.name, u.name, p.level, p.name
        """
        return self.execute_query(query, (country_id,), fetchall=True)

    # CREATE
    def create_cost(
        self,
        university_id: int,
        program_id: int,
        duration_years: float = None,
        tuition_usd: float = None,
        living_cost_index: float = None,
        rent_usd: float = None,
        visa_fee_usd: float = None,
        insurance_usd: float = None,
        exchange_rate: float = None,
    ) -> int:
        query = """
        INSERT INTO study_costs (
            university_id,
            program_id,
            duration_years,
            tuition_usd,
            living_cost_index,
            rent_usd,
            visa_fee_usd,
            insurance_usd,
            exchange_rate
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        params = (
            university_id,
            program_id,
            duration_years,
            tuition_usd,
            living_cost_index,
            rent_usd,
            visa_fee_usd,
            insurance_usd,
            exchange_rate,
        )
        return self.execute_insert(query, params)

    # UPDATE
    def update_cost(self, cost_id: int, **kwargs) -> int:
        """
        Update linh hoạt theo các field truyền vào:
        ví dụ: update_cost(5, tuition_usd=30000, rent_usd=1200)
        """
        allowed_fields = [
            "university_id",
            "program_id",
            "duration_years",
            "tuition_usd",
            "living_cost_index",
            "rent_usd",
            "visa_fee_usd",
            "insurance_usd",
            "exchange_rate",
        ]

        fields = []
        params = []

        for key, value in kwargs.items():
            if key in allowed_fields:
                fields.append(f"{key} = %s")
                params.append(value)

        if not fields:
            return 0

        params.append(cost_id)
        query = f"UPDATE study_costs SET {', '.join(fields)} WHERE id = %s"
        return self.execute_non_query(query, tuple(params))

    # DELETE
    def delete_cost(self, cost_id: int) -> int:
        query = "DELETE FROM study_costs WHERE id = %s"
        return self.execute_non_query(query, (cost_id,))
