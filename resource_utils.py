# resource_utils.py
import os, sys

def resource_path(relative_path: str) -> str:
    """
    Trả về đường dẫn tuyệt đối cho file resource (icon, image…)
    - Dùng được khi chạy python bình thường
    - Dùng được khi đã đóng gói bằng PyInstaller (._MEIPASS)
    """
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS  # thư mục tạm khi chạy .exe
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
