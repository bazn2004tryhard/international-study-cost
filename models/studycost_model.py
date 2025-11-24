from .base_model import BaseModel


class StudyCostModel(BaseModel):

    # ============================================================
    # READ ONE
    # ============================================================
    def get_cost_by_id(self, cost_id):
        query = """
            SELECT 
                s.*,
                u.name AS university,
                ci.name AS city,
                c.name AS country,
                p.name AS program,
                p.level AS level
            FROM study_costs s
            JOIN universities u ON s.university_id = u.id
            JOIN cities ci ON u.city_id = ci.id
            JOIN countries c ON ci.country_id = c.id
            JOIN programs p ON s.program_id = p.id
            WHERE s.id = %s
        """
        return self.execute_query(query, (cost_id,), fetchone=True)

    # ============================================================
    # READ BY UNIVERSITY
    # ============================================================
    def get_costs_by_university(self, university_id):
        query = """
            SELECT 
                s.*,
                u.name AS university,
                ci.name AS city,
                c.name AS country,
                p.name AS program,
                p.level AS level
            FROM study_costs s
            JOIN universities u ON s.university_id = u.id
            JOIN cities ci ON u.city_id = ci.id
            JOIN countries c ON ci.country_id = c.id
            JOIN programs p ON s.program_id = p.id
            WHERE u.id = %s
            ORDER BY p.name
        """
        return self.execute_query(query, (university_id,), fetchall=True)

    # ============================================================
    # READ BY COUNTRY
    # ============================================================
    def get_costs_by_country(self, country_id):
        query = """
            SELECT 
                s.id,
                c.name  AS country,
                ci.name AS city,
                u.name  AS university,
                p.name  AS program,
                p.level AS level,
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
            ORDER BY ci.name, u.name
        """
        return self.execute_query(query, (country_id,), fetchall=True)

    # ============================================================
    # CREATE
    # ============================================================
    def create_cost(
        self,
        university_id,
        program_id,
        duration_years,
        tuition_usd,
        living_cost_index,
        rent_usd,
        visa_fee_usd,
        insurance_usd,
        exchange_rate,
    ):
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
        return self.execute_insert(
            query,
            (
                university_id,
                program_id,
                duration_years,
                tuition_usd,
                living_cost_index,
                rent_usd,
                visa_fee_usd,
                insurance_usd,
                exchange_rate,
            ),
        )

    # ============================================================
    # UPDATE (Dynamic builder)
    # ============================================================
    def update_cost(self, cost_id, **fields):
        allowed = [
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

        updates = []
        values = []

        for k, v in fields.items():
            if k in allowed:
                updates.append(f"{k} = %s")
                values.append(v)

        if not updates:
            return 0

        query = f"UPDATE study_costs SET {', '.join(updates)} WHERE id = %s"
        values.append(cost_id)

        return self.execute_non_query(query, tuple(values))

    # ============================================================
    # DELETE
    # ============================================================
    def delete_cost(self, cost_id):
        query = "DELETE FROM study_costs WHERE id = %s"
        return self.execute_non_query(query, (cost_id,))

    # ============================================================
    # CHART QUERIES
    # ============================================================
    def get_tuition_by_university_and_level(self, country_id):
        query = """
            SELECT 
                u.name AS university,
                p.level,
                AVG(s.tuition_usd) AS avg_tuition
            FROM study_costs s
            JOIN universities u ON s.university_id = u.id
            JOIN cities ci ON u.city_id = ci.id
            JOIN countries c ON ci.country_id = c.id
            JOIN programs p ON s.program_id = p.id
            WHERE c.id = %s
            GROUP BY u.id, p.level
        """
        return self.execute_query(query, (country_id,), fetchall=True)

    def get_total_cost_by_university(self, country_id):
        query = """
            SELECT 
                u.name AS university,
                AVG(
                    IFNULL(s.tuition_usd,0)
                    + IFNULL(s.rent_usd,0) * 12
                    + IFNULL(s.visa_fee_usd,0)
                    + IFNULL(s.insurance_usd,0)
                ) AS avg_total_cost
            FROM study_costs s
            JOIN universities u ON s.university_id = u.id
            JOIN cities ci ON u.city_id = ci.id
            JOIN countries c ON ci.country_id = c.id
            WHERE c.id = %s
            GROUP BY u.id
        """
        return self.execute_query(query, (country_id,), fetchall=True)

    def get_avg_rent_by_city(self, country_id):
        query = """
            SELECT 
                ci.name AS city,
                AVG(s.rent_usd) AS avg_rent
            FROM study_costs s
            JOIN universities u ON s.university_id = u.id
            JOIN cities ci ON u.city_id = ci.id
            JOIN countries c ON ci.country_id = c.id
            WHERE c.id = %s
            GROUP BY ci.id
        """
        return self.execute_query(query, (country_id,), fetchall=True)

    def get_program_count_by_level(self, country_id):
        query = """
            SELECT 
                p.level,
                COUNT(*) AS program_count
            FROM study_costs s
            JOIN universities u ON s.university_id = u.id
            JOIN cities ci ON u.city_id = ci.id
            JOIN countries c ON ci.country_id = c.id
            JOIN programs p ON s.program_id = p.id
            WHERE c.id = %s
            GROUP BY p.level
        """
        return self.execute_query(query, (country_id,), fetchall=True)
    def get_all_study_costs(self):
        query = """
            SELECT 
                s.id,
                u.name AS university,
                ci.name AS city,
                c.name AS country,
                CONCAT(p.name, ' (', p.level, ')') AS program,
                p.level,
                s.duration_years,
                s.tuition_usd,
                s.living_cost_index,
                s.rent_usd,
                s.visa_fee_usd,
                s.insurance_usd,
                s.exchange_rate,
                s.university_id,
                s.program_id
            FROM study_costs s
            JOIN universities u ON s.university_id = u.id
            JOIN cities ci ON u.city_id = ci.id
            JOIN countries c ON ci.country_id = c.id
            JOIN programs p ON s.program_id = p.id
            ORDER BY c.name, ci.name, u.name, p.name
        """
        return self.execute_query(query, fetchall=True)