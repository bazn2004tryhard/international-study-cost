from models.program_model import ProgramModel


class ProgramController:
    def __init__(self):
        self.model = ProgramModel()

    def get_all_programs(self):
        return self.model.get_all_programs()

    def add_program(self, name, level):
        return self.model.create_program(name, level)

    def update_program(self, program_id, name=None, level=None):
        return self.model.update_program(program_id, name=name, level=level)

    def delete_program(self, program_id):
        return self.model.delete_program(program_id)

    def search_program(self, keyword=None, level=None):
        rows = self.get_all_programs()
        if not keyword and not level:
            return rows

        def match(row):
            by_keyword = True
            if keyword:
                by_keyword = keyword.lower() in row["name"].lower()

            by_level = True
            if level:
                by_level = row["level"] == level

            return by_keyword and by_level

        return [row for row in rows if match(row)]