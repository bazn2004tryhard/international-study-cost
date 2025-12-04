# controllers/studycost_controller.py

from models.studycost_model import StudyCostModel
from models.country_model import CountryModel
from models.city_model import CityModel
from models.university_model import UniversityModel
from models.program_model import ProgramModel


class StudyCostController:

    def __init__(self):
        self.model = StudyCostModel()
        self.country_model = CountryModel()
        self.city_model = CityModel()
        self.university_model = UniversityModel()
        self.program_model = ProgramModel()

    # ============================================================
    # READ
    # ============================================================
    def get_all_study_costs(self):
        """Lấy toàn bộ bản ghi study_costs (dùng cho bảng trong ManageStudyCostWindow)."""
        return self.model.get_all_study_costs()

    def get_cost_by_id(self, cost_id):
        """Lấy 1 bản ghi study_cost theo ID (dùng cho on_select trong view)."""
        return self.model.get_cost_by_id(cost_id)

    # ============================================================
    # CREATE
    # ============================================================
    def add_study_cost(
        self,
        university_id,
        program_id,
        duration=None,
        tuition=None,
        living_idx=None,
        rent=None,
        visa=None,
        insurance=None,
        exchange=None,
        **kwargs,
    ):
        """
        Thêm chi phí học mới.

        Tham số từ View:
            - university_id
            - program_id
            - duration        -> map sang duration_years
            - tuition         -> map sang tuition_usd
            - living_idx      -> map sang living_cost_index
            - rent            -> map sang rent_usd
            - visa            -> map sang visa_fee_usd
            - insurance       -> map sang insurance_usd
            - exchange        -> map sang exchange_rate
        **kwargs dùng để nuốt các tham số thừa (vd: parent=self) mà View gửi vào.
        """
        return self.model.create_cost(
            university_id=university_id,
            program_id=program_id,
            duration_years=duration,
            tuition_usd=tuition,
            living_cost_index=living_idx,
            rent_usd=rent,
            visa_fee_usd=visa,
            insurance_usd=insurance,
            exchange_rate=exchange,
        )

    # ============================================================
    # UPDATE
    # ============================================================
    def update_study_cost(
        self,
        cost_id,
        university_id=None,
        program_id=None,
        duration=None,
        tuition=None,
        living_idx=None,
        rent=None,
        visa=None,
        insurance=None,
        exchange=None,
        **kwargs,
    ):
        """
        Cập nhật chi phí học.
        Tham số giống như add_study_cost, map sang các cột tương ứng trong bảng.
        """
        return self.model.update_cost(
            cost_id,
            university_id=university_id,
            program_id=program_id,
            duration_years=duration,
            tuition_usd=tuition,
            living_cost_index=living_idx,
            rent_usd=rent,
            visa_fee_usd=visa,
            insurance_usd=insurance,
            exchange_rate=exchange,
        )

    # ============================================================
    # DELETE
    # ============================================================
    def delete_study_cost(self, cost_id, **kwargs):
        """
        Xóa một bản ghi chi phí học.
        **kwargs để nuốt tham số thừa (vd: parent=self) từ View.
        """
        return self.model.delete_cost(cost_id)

    # ============================================================
    # SEARCH
    # ============================================================
    def search_study_cost(self, keyword=None, university_id=None, program_id=None):
        """
        Lọc danh sách chi phí học theo:
            - keyword: tìm trong tên program hoặc university
            - university_id
            - program_id
        """
        rows = self.get_all_study_costs()
        if not keyword and not university_id and not program_id:
            return rows

        def match(row):
            by_keyword = True
            if keyword:
                kw = keyword.lower()
                by_keyword = (
                    kw in str(row.get("program", "")).lower()
                    or kw in str(row.get("university", "")).lower()
                )

            by_university = True
            if university_id:
                by_university = row.get("university_id") == university_id

            by_program = True
            if program_id:
                by_program = row.get("program_id") == program_id

            return by_keyword and by_university and by_program

        return [row for row in rows if match(row)]

    # ============================================================
    # HỖ TRỢ COMBOBOX (COUNTRY / CITY / UNIVERSITY / PROGRAM)
    # ============================================================
    def get_countries(self):
        return self.country_model.get_all_countries()

    def get_cities_by_country(self, country_id):
        return self.city_model.get_cities_by_country(country_id)

    def get_universities(self):
        return self.university_model.get_all_universities()

    def get_programs(self):
        return self.program_model.get_all_programs()
