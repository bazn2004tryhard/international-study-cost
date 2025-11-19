# models/program_model.py
from .base_model import BaseModel


class ProgramModel(BaseModel):

    # READ
    def get_all_programs(self):
        query = "SELECT id, name, level FROM programs ORDER BY level, name"
        return self.execute_query(query, fetchall=True)

    def get_program_by_id(self, program_id: int):
        query = "SELECT id, name, level FROM programs WHERE id = %s"
        return self.execute_query(query, (program_id,), fetchone=True)

    def get_programs_by_level(self, level: str):
        query = "SELECT id, name, level FROM programs WHERE level = %s ORDER BY name"
        return self.execute_query(query, (level,), fetchall=True)

    # CREATE
    def create_program(self, name: str, level: str) -> int:
        query = "INSERT INTO programs (name, level) VALUES (%s, %s)"
        return self.execute_insert(query, (name, level))

    # UPDATE
    def update_program(self, program_id: int, name: str = None, level: str = None) -> int:
        fields = []
        params = []

        if name is not None:
            fields.append("name = %s")
            params.append(name)
        if level is not None:
            fields.append("level = %s")
            params.append(level)

        if not fields:
            return 0

        params.append(program_id)
        query = f"UPDATE programs SET {', '.join(fields)} WHERE id = %s"
        return self.execute_non_query(query, tuple(params))

    # DELETE
    def delete_program(self, program_id: int) -> int:
        query = "DELETE FROM programs WHERE id = %s"
        return self.execute_non_query(query, (program_id,))
